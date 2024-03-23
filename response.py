import socket
import json
import os
import subprocess

HOST = ""
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen()

conn, addr = sock.accept()
data = conn.recv(1024)
message = json.loads(data.decode())

print(message["message"])

if message["message"] == "detect":
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    python_file_name = "tello_command.py"

    python_file_path = os.path.join(desktop_path, python_file_name)

    if os.path.isfile(python_file_path):
        subprocess.run(["python", python_file_path])
