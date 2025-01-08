import PyInstaller.__main__
import os
import platform

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Determine the operating system
os_type = platform.system()

# Define the icon based on the operating system
if os_type == "Darwin":  # macOS
    icon = "Comma.icns"
elif os_type == "Linux":  # Linux
    icon = "Comma.png"
else:  # Windows or others
    icon = "Comma.ico"

# Define the output and working directories
dist_path = os.path.join(current_dir, "dist", os_type)
work_path = os.path.join(current_dir, "build", os_type)

# Ensure the output and working directories exist
os.makedirs(dist_path, exist_ok=True)
os.makedirs(work_path, exist_ok=True)

PyInstaller.__main__.run([
    'note.py',  # your main script
    '--name=Comma',  # name of your executable
    '--windowed',  # prevents console window from appearing
    '--onefile',  # creates a single executable file
    f'--icon={icon}',  # path to your icon file (optional)
    '--add-data=README.md:.',  # add any additional files needed
    '--clean',  # clean PyInstaller cache
    '--noconfirm',  # replace output directory without asking
    f'--distpath={dist_path}',  # output directory
    f'--workpath={work_path}',  # working directory
    # '--splash=splash.png'  # optional splash screen
])