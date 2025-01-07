import os
import sys

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def ensure_app_dirs():
    """Ensure application directories exist"""
    app_data_dir = os.path.join(os.path.expanduser('~'), '.todo_app')
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
    return app_data_dir
