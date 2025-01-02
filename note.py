import sys
import json
from typing import List
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLineEdit, QLabel, QMessageBox, QScrollArea, QFrame, QDialog, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class Task:
    def __init__(self, text: str, completed: bool = False):
        self.text = text
        self.completed = completed

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks: List[Task] = []
        self.isDarkTheme = False
        self.initUI()
        self.loadTasks()

    def initUI(self):
        # Set global font
        globalFont = QFont()
        globalFont.setPointSize(14)
        QApplication.setFont(globalFont)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)

        # Top layout for task input and buttons
        topLayout = QHBoxLayout()
        topLayout.setSpacing(0)
        
        # Task input
        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Enter a new task...")
        self.taskInput.returnPressed.connect(self.addTask)
        
        # Buttons with icons
        changeThemeButton = QPushButton("Theme")
        changeThemeButton.setToolTip("Toggle light and dark themes.")
        changeThemeButton.clicked.connect(self.toggleTheme)
        changeThemeButton.setFont(QFont('', 10))
        changeThemeButton.setStyleSheet("padding: 10px;")

        clearTasksButton = QPushButton("AC")
        clearTasksButton.setToolTip("Clear all tasks from the list.")
        clearTasksButton.clicked.connect(self.clearAllTasks)
        clearTasksButton.setFont(QFont('', 10))
        clearTasksButton.setStyleSheet("padding: 10px;")
        
        topLayout.addWidget(self.taskInput)
        topLayout.addWidget(changeThemeButton)
        topLayout.addWidget(clearTasksButton)

        # Scrollable task area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        
        # Container for tasks
        self.taskContainer = QWidget()
        self.taskListLayout = QVBoxLayout(self.taskContainer)
        self.taskListLayout.setSpacing(0)
        self.scrollArea.setWidget(self.taskContainer)

        # Add layouts to main layout
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.scrollArea)

        # Set layout and window properties
        self.setLayout(mainLayout)
        self.setWindowTitle("To-Do")
        self.setGeometry(1464, 600, 450, 500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Apply initial theme
        self.applyTheme()

        # Set size policies
        self.taskInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def applyTheme(self):
        if self.isDarkTheme:
            # Dark theme
            self.setStyleSheet("""
                QWidget { 
                    background-color: #2C3E50; 
                    color: #ECF0F1; 
                }
                QLineEdit, QCheckBox { 
                    background-color: #34495E; 
                    color: #ECF0F1; 
                    border: 1px solid #2C3E50;
                }
                QCheckBox:checked {
                    text-decoration: line-through;
                    color: gray;
                }
                QPushButton { 
                    background-color: #FFFFFF; 
                    color: #000000; 
                    border: none;
                }
                QPushButton:hover {
                    background-color: #F0F0F0;
                }
            """)
        else:
            # Light theme
            self.setStyleSheet("""
                QWidget { 
                    background-color: #FFFFFF; 
                    color: #000000; 
                }
                QLineEdit, QCheckBox { 
                    background-color: #F1F1F1; 
                    color: #000000; 
                    border: 1px solid #CCCCCC;
                }
                QCheckBox:checked {
                    text-decoration: line-through;
                    color: gray;
                }
                QPushButton { 
                    background-color: #F1F1F1; 
                    color: #000000; 
                    border: none;
                }
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
            """)

    def addTask(self):
        task_text = self.taskInput.text().strip()
        if task_text:
            task = Task(task_text)  # Create the task directly
            self.tasks.append(task)  # Append the task to the tasks list
            self.updateTaskList()  # Update the task list display
            self.taskInput.clear()  # Clear the input field
            self.saveTasks()  # Save the tasks to the file

    def updateTaskList(self):
        # Clear existing task layout
        while self.taskListLayout.count():
            child = self.taskListLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Re-add tasks to the layout
        for task in self.tasks:
            taskLayout = QHBoxLayout()
            taskCheckBox = QCheckBox(task.text)
            taskCheckBox.setChecked(task.completed)
            taskCheckBox.stateChanged.connect(lambda state, t=task: self.toggleTaskCompletion(t, state))

            deleteButton = QPushButton('✖')
            deleteButton.setFixedWidth(40)
            deleteButton.clicked.connect(lambda _, t=task: self.deleteTask(t))

            editButton = QPushButton('✎')
            editButton.setFixedWidth(40)
            editButton.clicked.connect(lambda _, t=task, cb=taskCheckBox: self.editTask(t, cb))

            taskLayout.addWidget(taskCheckBox)
            taskLayout.addWidget(editButton)
            taskLayout.addWidget(deleteButton)

            taskFrame = QFrame()
            taskFrame.setLayout(taskLayout)
            self.taskListLayout.addWidget(taskFrame)

    def editTask(self, task, checkBox):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Task")
        layout = QVBoxLayout()

        textLabel = QLabel("Task:")
        textInput = QLineEdit(task.text)
        layout.addWidget(textLabel)
        layout.addWidget(textInput)

        buttonLayout = QHBoxLayout()
        okButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        layout.addLayout(buttonLayout)

        dialog.setLayout(layout)

        def onOkClicked():
            task.text = textInput.text().strip()
            checkBox.setText(task.text)
            dialog.accept()
            self.saveTasks()
            self.updateTaskList()

        okButton.clicked.connect(onOkClicked)
        cancelButton.clicked.connect(dialog.reject)

        dialog.exec_()

    def deleteTask(self, task):
        self.tasks.remove(task)
        self.updateTaskList()
        self.saveTasks()

    def toggleTaskCompletion(self, task, state):
        task.completed = (state == Qt.Checked)
        self.saveTasks()

    def toggleTheme(self):
        self.isDarkTheme = not self.isDarkTheme
        self.applyTheme()

    def clearAllTasks(self):
        reply = QMessageBox.question(self, 'Clear All Tasks', 'Are you sure you want to delete all tasks?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tasks.clear()
            self.updateTaskList()
            self.saveTasks()

    def saveTasks(self):
        tasks_to_save = [{'text': task.text, 'completed': task.completed} for task in self.tasks]
        try:
            with open('tasks.json', 'w') as f:
                json.dump(tasks_to_save, f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving tasks: {e}")

    def loadTasks(self):
        try:
            with open('tasks.json', 'r') as f:
                saved_tasks = json.load(f)
            for task_data in saved_tasks:
                task = Task(task_data['text'], task_data.get('completed', False))
                self.tasks.append(task)
            self.updateTaskList()
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Warning", "Error loading tasks: JSON file is corrupted.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading tasks: {e}")

def main():
    app = QApplication(sys.argv)
    
    # Fallback for icon themes
    if not QIcon.hasThemeIcon("color-management"):
        # You can add your own fallback icons or paths here
        pass
    
    todoApp = ToDoApp()
    todoApp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()