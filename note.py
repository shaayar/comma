"""
Comma Note-Taking App
------------------------
A feature-rich todo list application built with PyQt5, implementing:
- Task management with priorities and timestamps
- Theme switching capability
- Configuration persistence
- Task import/export functionality
- Observable pattern for state management
- Custom widgets for better UI/UX
"""

import sys
import json
from typing import List, Callable, Optional, Dict
from datetime import datetime
from dataclasses import dataclass, field
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QLineEdit, QLabel, QMessageBox,
    QScrollArea, QFrame, QDialog, QSizePolicy, QComboBox,
    QMenuBar, QMenu, QAction, QFileDialog, QDesktopWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from todo_resources import get_resource_path, ensure_app_dirs
class Config:
    """
    Manages application configuration and persistence.
    Handles window position, size, theme preference, and other settings.
    Uses JSON for storage to maintain settings between sessions.
    """
    def __init__(self):
        # Initialize with default values that will be used if no saved config exists
        self.theme = "light"  # Default theme
        self.window_position = None  # Will be set based on screen center if None
        self.window_size = (450, 500)  # Default window dimensions
        self.last_priority = "Normal"  # Remember last used priority for convenience
        
    def save(self) -> None:
        """
        Saves current configuration to JSON file.
        Handles potential file write errors gracefully.
        """
        config = {
            'theme': self.theme,
            'window_position': self.window_position,
            'window_size': self.window_size,
            'last_priority': self.last_priority
        }
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f)
        except Exception as e:
            # Log error but don't crash - app can continue with current settings
            print(f"Error saving configuration: {e}")
            
    @classmethod
    def load(cls) -> 'Config':
        """
        Creates and loads a Config instance from saved file.
        Returns a new Config with default values if no saved config exists.
        """
        config = cls()
        try:
            with open('config.json', 'r') as f:
                saved_config = json.load(f)
                # Use get() with defaults to handle missing or corrupt config entries
                config.theme = saved_config.get('theme', 'light')
                config.window_position = saved_config.get('window_position')
                config.window_size = saved_config.get('window_size', (450, 500))
                config.last_priority = saved_config.get('last_priority', 'Normal')
        except FileNotFoundError:
            # First time running app - use defaults
            pass
        return config

@dataclass
class Task:
    """
    Represents a single todo task with metadata.
    Uses @dataclass for automatic generation of __init__, __repr__, etc.
    Tracks creation and completion times for task history.
    """
    text: str
    priority: str
    completed: bool = False
    # Use field(default_factory=...) to ensure each task gets its own timestamp
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def complete(self) -> None:
        """Marks task complete and records completion time"""
        if not self.completed:
            self.completed = True
            self.completed_at = datetime.now()
            
    def uncomplete(self) -> None:
        """Resets task to incomplete state"""
        self.completed = False
        self.completed_at = None
        
    @property
    def is_high_priority(self) -> bool:
        """Convenience property to check priority level"""
        return self.priority == "High"
    
    def to_dict(self) -> dict:
        """
        Converts task to dictionary for JSON serialization.
        Handles datetime conversion to ISO format strings.
        """
        return {
            'text': self.text,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Creates Task instance from dictionary data.
        Handles conversion of ISO format strings back to datetime objects.
        """
        task = cls(
            text=data['text'],
            priority=data['priority'],
            completed=data['completed']
        )
        task.created_at = datetime.fromisoformat(data['created_at'])
        if data['completed_at']:
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        return task

class TaskManager:
    """
    Manages the collection of tasks using the Observer pattern.
    Handles task operations and persistence, notifying observers of changes.
    """
    def __init__(self):
        self.tasks: List[Task] = []
        # List of callback functions to be notified when tasks change
        self._observers: List[Callable] = []
        
    def add_observer(self, callback: Callable) -> None:
        """Registers a callback to be notified of task changes"""
        self._observers.append(callback)
        
    def notify_observers(self) -> None:
        """Notifies all registered observers of task changes"""
        for observer in self._observers:
            observer()
            
    def add_task(self, task: Task) -> None:
        """Adds task and notifies observers"""
        self.tasks.append(task)
        self.notify_observers()
        
    def remove_task(self, task: Task) -> None:
        """Removes task and notifies observers"""
        self.tasks.remove(task)
        self.notify_observers()
        
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Filters tasks by priority level"""
        return [task for task in self.tasks if task.priority == priority]
    
    def save_tasks(self) -> None:
        """
        Saves all tasks to JSON file.
        Converts tasks to dictionary format for serialization.
        """
        try:
            tasks_data = [task.to_dict() for task in self.tasks]
            with open('tasks.json', 'w') as f:
                json.dump(tasks_data, f)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self) -> None:
        """
        Loads tasks from JSON file.
        Converts serialized data back to Task objects.
        """
        try:
            with open('tasks.json', 'r') as f:
                tasks_data = json.load(f)
            self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
            self.notify_observers()
        except FileNotFoundError:
            # No saved tasks yet - start with empty list
            pass
        except Exception as e:
            print(f"Error loading tasks: {e}")

class TaskWidget(QFrame):
    """
    Custom widget for displaying a single task.
    Provides interface for task interaction (edit, delete, complete).
    """
    deleted = pyqtSignal(Task)
    edited = pyqtSignal(Task)
    status_changed = pyqtSignal(Task)

    def __init__(self, task: Task):
        super().__init__()
        self.task = task
        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI components for the task widget.
        """
        layout = QHBoxLayout()
        self.checkbox = QCheckBox(self.task.text)
        self.checkbox.setChecked(self.task.completed)
        self.checkbox.stateChanged.connect(self.toggle_task)

        # Priority label with dynamic height using size policy
        self.priority_label = QLabel(self.task.priority)
        self.priority_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Set size policy
        self.priority_label.setMaximumHeight(20)  # Set a maximum height
        self.priority_label.setAlignment(Qt.AlignCenter)  # Center the text

        # Edit button
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit_task)

        # Delete button
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_task)

        # Add widgets to the layout
        layout.addWidget(self.checkbox)
        layout.addWidget(self.priority_label)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def toggle_task(self):
        """Handles task completion toggle and emits status change."""
        if self.checkbox.isChecked():
            self.task.complete()
        else:
            self.task.uncomplete()
        self.status_changed.emit(self.task)

    def edit_task(self):
        """Opens the edit dialog for the task."""
        self.edited.emit(self.task)

    def delete_task(self):
        """Emits a signal to delete the task."""
        self.deleted.emit(self.task)
class EditTaskDialog(QDialog):
    """
    Dialog for editing an existing task.
    Provides fields for modifying task text and priority.
    """
    def __init__(self, task: Task, parent=None):
        super().__init__(parent)  # Properly pass parent to QDialog
        self.task = task
        self.setup_ui()

    def setup_ui(self) -> None:
        """Creates and arranges the dialog's UI components."""
        self.setWindowTitle("Edit Task")
        layout = QVBoxLayout(self)

        # Task text input
        text_label = QLabel("Task:")
        self.text_input = QLineEdit(self.task.text)
        self.text_input.setPlaceholderText("Enter task description...")

        # Priority selection
        priority_label = QLabel("Priority:")
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Normal", "High"])
        self.priority_combo.setCurrentText(self.task.priority)

        # Dialog buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        # Assemble layout
        layout.addWidget(text_label)
        layout.addWidget(self.text_input)
        layout.addWidget(priority_label)
        layout.addWidget(self.priority_combo)
        layout.addLayout(button_layout)

        # Inherit theme from parent window
        if self.parent():
            self.setStyleSheet(self.parent().styleSheet())
class ToDoApp(QMainWindow):
    """
    Main application window.
    Coordinates between UI components and task management.
    Handles persistence of application state and user preferences.
    """
    def __init__(self):
        super().__init__()
        # Initialize configuration and task management
        self.config = Config.load()
        self.task_manager = TaskManager()
        
        # Set up UI and load saved state
        self.setup_ui()
        self.task_manager.load_tasks()
        
        # Register for task updates
        self.task_manager.add_observer(self.update_task_list)
        
    def setup_ui(self) -> None:
        """
        Creates and arranges the main window's UI components.
        Sets up menu bar, input area, and task list.
        Restores window geometry from saved configuration.
        """
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Set up UI components
        self.create_menu_bar()
        self.setup_input_area(layout)
        self.setup_task_list(layout)
        
        # Configure window
        self.setWindowTitle("Enhanced Todo")
        self.apply_theme()
        
        # Restore or center window
        if self.config.window_position:
            self.move(*self.config.window_position)
        else:
            # Center window on screen
            center = QDesktopWidget().availableGeometry().center()
            self.move(center.x() - self.width()//2, center.y() - self.height()//2)
            
        self.resize(*self.config.window_size)
        
    def create_menu_bar(self) -> None:
        """
        Creates application menu bar with file and view menus.
        Sets up keyboard shortcuts for common actions.
        """
        menubar = self.menuBar()
        
        # File menu for task management
        file_menu = menubar.addMenu('&File')
        
        export_action = QAction('&Export Tasks', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_tasks)
        
        file_menu.addAction(export_action)
        
        # View menu for appearance options
        view_menu = menubar.addMenu('&View')
        
        theme_action = QAction('Toggle &Theme', self)
        theme_action.setShortcut('Ctrl+T')
        theme_action.triggered.connect(self.toggle_theme)
        
        view_menu.addAction(theme_action)
        
    def setup_input_area(self, parent_layout: QVBoxLayout) -> None:
        """Creates task input area with text field, priority selector, and add button"""
        input_layout = QHBoxLayout()
        
        # Task input field
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.task_input.returnPressed.connect(self.add_task)
        
        # Priority selection dropdown
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Normal", "High"])
        self.priority_combo.setCurrentText(self.config.last_priority)
        
        # Add button
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_task)
        
        # Assemble layout
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.priority_combo)
        input_layout.addWidget(add_btn)
        
        parent_layout.addLayout(input_layout)
        
    def setup_task_list(self, parent_layout: QVBoxLayout) -> None:
        """Creates scrollable area for task list"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setSpacing(5)

        # Continuing from the previous setup_task_list method...
        self.scroll_area.setWidget(self.task_container)
        parent_layout.addWidget(self.scroll_area)

    def add_task(self) -> None:
        """
        Handles the creation of a new task.
        Validates input, creates task object, and updates UI.
        Saves task state and user preferences after addition.
        """
        # Get and validate task text
        text = self.task_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter a task description.")
            return
            
        # Get current priority and save as last used
        priority = self.priority_combo.currentText()
        self.config.last_priority = priority
        self.config.save()
        
        # Create and add new task
        task = Task(text, priority)
        self.task_manager.add_task(task)
        self.task_manager.save_tasks()
        
        # Clear input field for next task
        self.task_input.clear()
        
    def update_task_list(self) -> None:
        """
        Refreshes the task list display.
        Removes existing task widgets and creates new ones for current tasks.
        Connects signal handlers for task interactions.
        """
        # Remove existing task widgets
        while self.task_layout.count():
            widget = self.task_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        # Create widgets for current tasks
        for task in self.task_manager.tasks:
            task_widget = TaskWidget(task)
            # Connect interaction signals to appropriate handlers
            task_widget.deleted.connect(self.delete_task)
            task_widget.edited.connect(self.edit_task)
            task_widget.status_changed.connect(self.save_tasks)
            self.task_layout.addWidget(task_widget)
            
    def delete_task(self, task: Task) -> None:
        """
        Removes a task from the task list.
        Updates persistent storage after deletion.
        """
        self.task_manager.remove_task(task)
        self.task_manager.save_tasks()
        
    def edit_task(self, task: Task) -> None:
        """
        Opens edit dialog for task modification.
        Updates task and persistent storage if changes are accepted.
        """
        dialog = EditTaskDialog(task, self)
        if dialog.exec_() == QDialog.Accepted:  # Ensure dialog is accepted
            new_text = dialog.text_input.text().strip()
            new_priority = dialog.priority_combo.currentText()

            # Validate task text
            if not new_text:
                QMessageBox.warning(self, "Warning", "Task description cannot be empty.")
                return

            # Update task with new values
            task.text = new_text
            task.priority = new_priority

            # Save tasks and update UI
            self.task_manager.save_tasks()
            self.update_task_list()
            
    def save_tasks(self, task: Optional[Task] = None) -> None:
        """
        Saves current task state to persistent storage.
        Accepts variable arguments to work as a slot for multiple signals.
        """
        self.task_manager.save_tasks()
        
    def export_tasks(self) -> None:
        """
        Exports tasks to a user-specified JSON file.
        Opens file dialog for destination selection.
        """
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Tasks",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if filename:
            try:
                # Ensure filename has .json extension
                if not filename.endswith('.json'):
                    filename += '.json'
                
                # Export tasks to selected file
                tasks_data = [task.to_dict() for task in self.task_manager.tasks]
                with open(filename, 'w') as f:
                    json.dump(tasks_data, f, indent=2)
                    
                QMessageBox.information(self, "Success", "Tasks exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export tasks: {str(e)}")

    def import_tasks(self) -> None:
        """
        Imports tasks from a user-selected JSON file.
        Validates file format and merges with existing tasks.
        """
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Import Tasks",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    imported_data = json.load(f)
                
                # Validate and convert imported data
                imported_tasks = [Task.from_dict(task_data) for task_data in imported_data]
                
                # Add imported tasks to existing ones
                for task in imported_tasks:
                    self.task_manager.add_task(task)
                
                QMessageBox.information(self, "Success", 
                    f"Successfully imported {len(imported_tasks)} tasks!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import tasks: {str(e)}")

    def toggle_theme(self) -> None:
        """
        Switches between light and dark themes.
        Updates configuration and persists theme preference.
        """
        self.config.theme = "dark" if self.config.theme == "light" else "light"
        self.apply_theme()
        self.config.save()

    def apply_theme(self) -> None:
        """
        Applies the current theme to the application.
        Sets colors and styles for all UI components.
        """
        if self.config.theme == "dark":
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2C3E50;
                    color: #ECF0F1;
                }
                QLineEdit, QComboBox {
                    background-color: #34495E;
                    color: #ECF0F1;
                    border: 1px solid #2C3E50;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
                QCheckBox {
                    spacing: 5px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QScrollArea, QFrame {
                    border: 1px solid #34495E;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: white;
                    color: #2C3E50;
                }
                QLineEdit, QComboBox {
                    background-color: #F5F6FA;
                    border: 1px solid #DFE4EA;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
                QCheckBox {
                    spacing: 5px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QScrollArea, QFrame {
                    border: 1px solid #DFE4EA;
                }
            """)

    def closeEvent(self, event) -> None:
        """
        Handles application shutdown.
        Saves current window geometry and task state before closing.
        """
        # Save window geometry
        self.config.window_position = (self.x(), self.y())
        self.config.window_size = (self.width(), self.height())
        self.config.save()
        
        # Save tasks
        self.task_manager.save_tasks()
        
        # Accept the close event
        event.accept()

def main():
    """
    Application entry point.
    Sets up the application instance and main window.
    """
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont('Segoe UI', 10))
    
    # Create and show main window
    todo_app = ToDoApp()
    todo_app.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()