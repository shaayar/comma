import sys
import json
from typing import List, Dict
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLineEdit, QLabel, QMessageBox, QScrollArea, QFrame, QDialog, QComboBox)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem

class Task:
    def __init__(self, text: str, completed: bool = False, priority: str = 'Medium', category: str = 'General'):
        self.text = text
        self.completed = completed
        self.priority = priority  # Options: Low, Medium, High
        self.category = category

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks: List[Task] = []
        self.isDarkTheme = False
        self.taskCounterLabel = QLabel("Total Tasks: 0 | Completed: 0 | Incomplete: 0")
        self.initUI()
        self.loadTasks()

    def initUI(self):
        # Set global font
        globalFont = QFont()
        globalFont.setPointSize(12)
        QApplication.setFont(globalFont)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        
        # Add filter dropdowns to the top layout
        self.priorityFilter = QComboBox()
        self.priorityFilter.addItems(['All Priorities', 'Low', 'Medium', 'High'])
        self.priorityFilter.currentTextChanged.connect(self.applyFilter)

        self.categoryFilter = QComboBox()
        self.categoryFilter.addItems(['All Categories', 'General'])  # Dynamically populate
        self.categoryFilter.currentTextChanged.connect(self.applyFilter)

        # Top layout for task input and buttons
        topLayout = QHBoxLayout()
        topLayout.setSpacing(0)
        
        # Task input
        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Enter a new task...")
        
        # Set font specifically for task input
        inputFont = QFont()
        inputFont.setPointSize(13)  # Larger font size
        self.taskInput.setFont(inputFont)
    
        self.taskInput.returnPressed.connect(self.addTask)
        
        # Buttons with icons
        changeThemeButton = QPushButton()
        changeThemeButton.setIcon(QIcon.fromTheme("color-management", QIcon(":/icons/theme-icon.png")))
        changeThemeButton.setToolTip("Theme")
        changeThemeButton.clicked.connect(self.toggleTheme)

        clearTasksButton = QPushButton()
        clearTasksButton.setIcon(QIcon.fromTheme("edit-clear", QIcon(":/icons/clear-icon.png")))
        clearTasksButton.setToolTip("Clear")
        clearTasksButton.clicked.connect(self.clearAllTasks)
        
        # Add these after the existing buttons
        exportButton = QPushButton()
        exportButton.setIcon(QIcon.fromTheme("document-export", QIcon(":/icons/export-icon.png")))
        exportButton.setToolTip("Export Tasks")
        exportButton.clicked.connect(self.exportTasks)

        importButton = QPushButton()
        importButton.setIcon(QIcon.fromTheme("document-import", QIcon(":/icons/import-icon.png")))
        importButton.setToolTip("Import Tasks")
        importButton.clicked.connect(self.importTasks)

        statsButton = QPushButton()
        statsButton.setIcon(QIcon.fromTheme("view-statistics", QIcon(":/icons/stats-icon.png")))
        statsButton.setToolTip("Task Statistics")
        statsButton.clicked.connect(self.showTaskStatistics)
        
        topLayout.addWidget(self.taskInput)
        topLayout.addWidget(changeThemeButton)
        topLayout.addWidget(clearTasksButton)
        topLayout.addWidget(self.priorityFilter)
        topLayout.addWidget(self.categoryFilter)
        topLayout.addWidget(exportButton)
        topLayout.addWidget(importButton)
        topLayout.addWidget(statsButton)

        # Scrollable task area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        
        # Container for tasks
        self.taskContainer = QWidget()
        self.taskListLayout = QVBoxLayout(self.taskContainer)
        self.taskListLayout.setSpacing(0)  # Remove spacing between tasks
        self.scrollArea.setWidget(self.taskContainer)

        # Add layouts to main layout
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.scrollArea)
        
        self.taskCounterLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.taskCounterLabel)

        # Set layout and window properties
        self.setLayout(mainLayout)
        self.setWindowTitle("To-Do")
        self.setGeometry(300, 300, 900, 500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Apply initial theme
        self.applyTheme()

    def applyTheme(self):
        if self.isDarkTheme:
            # Dark theme
            self.setStyleSheet("""
                QWidget { 
                    background-color: #2C3E50; 
                    color: #ECF0F1; 
                    font-size: 12px;
                }
                QLineEdit, QCheckBox { 
                    background-color: #34495E; 
                    color: #ECF0F1; 
                    border: 1px solid #2C3E50;
                    font-size: 12px;
                }
                QCheckBox:checked {
                    text-decoration: line-through;
                    color: gray;
                }
                QPushButton { 
                    background-color: #FFFFFF; 
                    color: #000000; 
                    border: none;
                    font-size: 12px;
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
                    font-size: 12px;
                }
                QLineEdit, QCheckBox { 
                    background-color: #F1F1F1; 
                    color: #000000; 
                    border: 1px solid #CCCCCC;
                    font-size: 12px;
                }
                QCheckBox:checked {
                    text-decoration: line-through;
                    color: gray;
                }
                QPushButton { 
                    background-color: #F1F1F1; 
                    color: #000000; 
                    border: none;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
            """)

    def addTask(self):
        task_text = self.taskInput.text().strip()
        if task_text:
            # Create dialog for additional task details
            dialog = QDialog(self)
            dialog.setWindowTitle("Add Task Details")
            layout = QVBoxLayout()

            # Task text
            textLabel = QLabel("Task:")
            textInput = QLineEdit(task_text)
            layout.addWidget(textLabel)
            layout.addWidget(textInput)

            # Priority selection
            priorityLabel = QLabel("Priority:")
            priorityCombo = QComboBox()
            priorityCombo.addItems(['Low', 'Medium', 'High'])
            priorityCombo.setCurrentText('Medium')
            layout.addWidget(priorityLabel)
            layout.addWidget(priorityCombo)

            # Category input
            categoryLabel = QLabel("Category:")
            categoryInput = QLineEdit()
            categoryInput.setPlaceholderText("Optional")
            layout.addWidget(categoryLabel)
            layout.addWidget(categoryInput)

            # Buttons
            buttonLayout = QHBoxLayout()
            okButton = QPushButton("OK")
            cancelButton = QPushButton("Cancel")
            buttonLayout.addWidget(okButton)
            buttonLayout.addWidget(cancelButton)
            layout.addLayout(buttonLayout)

            dialog.setLayout(layout)

            # Button connections
            def onOkClicked():
                final_text = textInput.text().strip()
                final_priority = priorityCombo.currentText()
                final_category = categoryInput.text().strip() or 'General'

                if final_text:
                    # Create task with additional details
                    task = Task(final_text, priority=final_priority, category=final_category)
                    self.tasks.append(task)
                    
                    # Create task layout
                    taskLayout = QHBoxLayout()
                    
                    # Modify checkbox to show priority and category
                    taskCheckBox = QCheckBox(f"{final_text} [{final_priority}] - {final_category}")
                    taskCheckBox.setChecked(task.completed)
                    taskCheckBox.stateChanged.connect(lambda state, t=task: self.toggleTaskCompletion(t, state))
                    
                    # Delete button
                    deleteButton = QPushButton('✖')
                    deleteButton.setFixedWidth(30)
                    deleteButton.clicked.connect(lambda _, layout=taskLayout, t=task: self.deleteTask(t, layout))
                    
                    # Edit button
                    editButton = QPushButton('✎')
                    editButton.setFixedWidth(30)
                    editButton.clicked.connect(lambda _, t=task, cb=taskCheckBox: self.editTask(t, cb))
                    
                    # Add widgets to layout
                    taskLayout.addWidget(taskCheckBox)
                    taskLayout.addWidget(editButton)
                    taskLayout.addWidget(deleteButton)
                    
                    # Create frame
                    taskFrame = QFrame()
                    taskFrame.setLayout(taskLayout)
                    
                    # Add to task list
                    self.taskListLayout.addWidget(taskFrame)
                    
                    dialog.accept()
                
            okButton.clicked.connect(onOkClicked)
            cancelButton.clicked.connect(dialog.reject)

            dialog.exec_()
            
            # Clear input field
            self.taskInput.clear()
            
            # Save tasks and update the counter
            self.saveTasks()
            self.updateTaskCounter()

    def editTask(self, task, checkBox):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Task")
        layout = QVBoxLayout()

        # Task text
        textLabel = QLabel("Task:")
        textInput = QLineEdit(task.text)
        layout.addWidget(textLabel)
        layout.addWidget(textInput)

        # Priority selection
        priorityLabel = QLabel("Priority:")
        priorityCombo = QComboBox()
        priorityCombo.addItems(['Low', 'Medium', 'High'])
        priorityCombo.setCurrentText(task.priority)
        layout.addWidget(priorityLabel)
        layout.addWidget(priorityCombo)

        # Category input
        categoryLabel = QLabel("Category:")
        categoryInput = QLineEdit(task.category)
        layout.addWidget(categoryLabel)
        layout.addWidget(categoryInput)

        # Buttons
        buttonLayout = QHBoxLayout()
        okButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        layout.addLayout(buttonLayout)

        dialog.setLayout(layout)

        def onOkClicked():
            # Update task details
            task.text = textInput.text().strip()
            task.priority = priorityCombo.currentText()
            task.category = categoryInput.text().strip() or 'General'

            # Update checkbox text
            checkBox.setText(f"{task.text} [{task.priority}] - {task.category}")
            
            dialog.accept()
            self.saveTasks()

        okButton.clicked.connect(onOkClicked)
        cancelButton.clicked.connect(dialog.reject)

        dialog.exec_()

    def deleteTask(self, task, layout):
        # Remove task from tasks list
        self.tasks.remove(task)
        
        # Find the parent widget and remove it
        parent = layout.parentWidget()
        if parent:
            parent.deleteLater()
        
        # Save updated tasks and update task count
        self.saveTasks()
        self.updateTaskCounter()

    def toggleTaskCompletion(self, task, state):
        # Update task completion status
        task.completed = (state == Qt.Checked)
        
        # Save tasks and update task count
        self.saveTasks()
        self.updateTaskCounter()

    def toggleTheme(self):
        # Toggle between dark and light theme
        self.isDarkTheme = not self.isDarkTheme
        self.applyTheme()

    def clearAllTasks(self):
        # Show confirmation dialog
        reply = QMessageBox.question(self, 'Clear All Tasks', 'Are you sure you want to delete all tasks?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Clear tasks list
            self.tasks.clear()
            
            # Remove all widgets from task layout
            while self.taskListLayout.count():
                child = self.taskListLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Save (empty) tasks and update task count
            self.saveTasks()
            self.updateTaskCounter()

    def applyFilter(self):
        priority = self.priorityFilter.currentText()
        category = self.categoryFilter.currentText()
        
        priority = priority if priority != 'All Priorities' else None
        category = category if category != 'All Categories' else None
        
        self.filterTasks(priority, category)

    def filterTasks(self, priority=None, category=None):
        # Clear current task list
        while self.taskListLayout.count():
            child = self.taskListLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Repopulate with filtered tasks
        for task in self.tasks:
            if (priority is None or task.priority == priority) and \
            (category is None or task.category == category):
                # Create task layout (similar to existing code)
                taskLayout = QHBoxLayout()
                
                taskCheckBox = QCheckBox(f"{task.text} [{task.priority}] - {task.category}")
                taskCheckBox.setChecked(task.completed)
                taskCheckBox.stateChanged.connect(lambda state, t=task: self.toggleTaskCompletion(t, state))
                
                deleteButton = QPushButton('✖')
                deleteButton.setFixedWidth(30)
                deleteButton.clicked.connect(lambda _, layout=taskLayout, t=task: self.deleteTask(t, layout))
                
                editButton = QPushButton('✎')
                editButton.setFixedWidth(30)
                editButton.clicked.connect(lambda _, t=task, cb=taskCheckBox: self.editTask(t, cb))
                
                taskLayout.addWidget(taskCheckBox)
                taskLayout.addWidget(editButton)
                taskLayout.addWidget(deleteButton)
                
                taskFrame = QFrame()
                taskFrame.setLayout(taskLayout)
                
                self.taskListLayout.addWidget(taskFrame)

    def saveTasks(self):
        # Convert tasks to a list of dictionaries with new attributes
        tasks_to_save = [
            {
                'text': task.text, 
                'completed': task.completed,
                'priority': task.priority,
                'category': task.category
            } for task in self.tasks
        ]
        
        try:
            with open('tasks.json', 'w') as f:
                json.dump(tasks_to_save, f)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def loadTasks(self):
        try:
            with open('tasks.json', 'r') as f:
                saved_tasks = json.load(f)
            
            for task_data in saved_tasks:
                task = Task(
                    task_data['text'], 
                    task_data.get('completed', False),
                    task_data.get('priority', 'Medium'),
                    task_data.get('category', 'General')
                )
                self.tasks.append(task)
                
                # Create task layout
                taskLayout = QHBoxLayout()
                
                taskCheckBox = QCheckBox(f"{task.text} [{task.priority}] - {task.category}")
                taskCheckBox.setChecked(task.completed)
                taskCheckBox.stateChanged.connect(lambda state, t=task: self.toggleTaskCompletion(t, state))
                
                deleteButton = QPushButton('✖')
                deleteButton.setFixedWidth(30)
                deleteButton.clicked.connect(lambda _, layout=taskLayout, t=task: self.deleteTask(t, layout))
                
                editButton = QPushButton('✎')
                editButton.setFixedWidth(30)
                editButton.clicked.connect(lambda _, t=task, cb=taskCheckBox: self.editTask(t, cb))
                
                taskLayout.addWidget(taskCheckBox)
                taskLayout.addWidget(editButton)
                taskLayout.addWidget(deleteButton)
                
                taskFrame = QFrame()
                taskFrame.setLayout(taskLayout)
                
                self.taskListLayout.addWidget(taskFrame)
        
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading tasks: {e}")

        self.updateTaskCounter()

    def updateTaskCounter(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.completed)
        incomplete_tasks = total_tasks - completed_tasks
        
        self.taskCounterLabel.setText(f"Total Tasks: {total_tasks} | Completed: {completed_tasks} | Incomplete: {incomplete_tasks}")

    def exportTasks(self):
        from PyQt5.QtWidgets import QFileDialog
        
        # Open file dialog to choose export location
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Tasks", "", "JSON Files (*.json)")
        
        if file_path:
            try:
                # Convert tasks to a list of dictionaries
                tasks_to_export = [
                    {
                        'text': task.text, 
                        'completed': task.completed,
                        'priority': task.priority,
                        'category': task.category
                    } for task in self.tasks
                ]
                
                # Write tasks to the selected file
                with open(file_path, 'w') as f:
                    json.dump(tasks_to_export, f, indent=4)
                
                QMessageBox.information(self, "Export Successful", f"Tasks exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export tasks: {str(e)}")

    def importTasks(self):
        from PyQt5.QtWidgets import QFileDialog
        
        # Open file dialog to choose import file
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Tasks", "", "JSON Files (*.json)")
        
        if file_path:
            try:
                # Read tasks from the selected file
                with open(file_path, 'r') as f:
                    imported_tasks = json.load(f)
                
                # Clear existing tasks
                self.tasks.clear()
                
                # Clear existing task layout
                while self.taskListLayout.count():
                    child = self.taskListLayout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                
                # Add imported tasks
                for task_data in imported_tasks:
                    task = Task(
                        task_data['text'], 
                        task_data.get('completed', False),
                        task_data.get('priority', 'Medium'),
                        task_data.get('category', 'General')
                    )
                    self.tasks.append(task)
                    
                    # Create task layout (similar to loadTasks method)
                    taskLayout = QHBoxLayout()
                    
                    taskCheckBox = QCheckBox(f"{task.text} [{task.priority}] - {task.category}")
                    taskCheckBox.setChecked(task.completed)
                    taskCheckBox.stateChanged.connect(lambda state, t=task: self.toggleTaskCompletion(t, state))
                    
                    deleteButton = QPushButton('✖')
                    deleteButton.setFixedWidth(30)
                    deleteButton.clicked.connect(lambda _, layout=taskLayout, t=task: self.deleteTask(t, layout))
                    
                    editButton = QPushButton('✎')
                    editButton.setFixedWidth(30)
                    editButton.clicked.connect(lambda _, t=task, cb=taskCheckBox: self.editTask(t, cb))
                    
                    taskLayout.addWidget(taskCheckBox)
                    taskLayout.addWidget(editButton)
                    taskLayout.addWidget(deleteButton)
                    
                    taskFrame = QFrame()
                    taskFrame.setLayout(taskLayout)
                    
                    self.taskListLayout.addWidget(taskFrame)
                
                # Save imported tasks
                self.saveTasks()
                
                QMessageBox.information(self, "Import Successful", f"Tasks imported from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import tasks: {str(e)}")

    def showTaskStatistics(self):
        # Create statistics dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Task Statistics")
        layout = QVBoxLayout()

        # Calculate statistics
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.completed)
        incomplete_tasks = total_tasks - completed_tasks

        # Priority breakdown
        priority_counts = {
            'Low': sum(1 for task in self.tasks if task.priority == 'Low'),
            'Medium': sum(1 for task in self.tasks if task.priority == 'Medium'),
            'High': sum(1 for task in self.tasks if task.priority == 'High')
        }

        # Category breakdown
        category_counts = {}
        for task in self.tasks:
            category_counts[task.category] = category_counts.get(task.category, 0) + 1

        # Create statistics labels
        stats_labels = [
            f"Total Tasks: {total_tasks}",
            f"Completed Tasks: {completed_tasks}",
            f"Incomplete Tasks: {incomplete_tasks}",
            "\nPriority Breakdown:",
            f"Low Priority: {priority_counts['Low']}",
            f"Medium Priority: {priority_counts['Medium']}",
            f"High Priority: {priority_counts['High']}",
            "\nCategory Breakdown:"
        ]

        # Add category breakdown
        for category, count in category_counts.items():
            stats_labels.append(f"{category}: {count}")

        # Add labels to dialog
        for stat in stats_labels:
            label = QLabel(stat)
            layout.addWidget(label)

        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()

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