import os
import subprocess

message = input("enter message")

if message == "detect":
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    python_file_name = "tello_command.py"

    python_file_path = os.path.join(desktop_path, python_file_name)

    if os.path.isfile(python_file_path):
        subprocess.run(["python", python_file_path])