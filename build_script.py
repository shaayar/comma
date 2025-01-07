import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'note.py',  # your main script
    '--name=Comma',  # name of your executable
    '--windowed',  # prevents console window from appearing
    '--onefile',  # creates a single executable file
    '--icon=Comma.ico',  # path to your icon file (optional)
    '--add-data=README.md:.',  # add any additional files needed
    '--clean',  # clean PyInstaller cache
    '--noconfirm',  # replace output directory without asking
    f'--distpath={os.path.join(current_dir, "dist")}',  # output directory
    f'--workpath={os.path.join(current_dir, "build")}',  # working directory
    '--splash=splash.png'  # optional splash screen
])