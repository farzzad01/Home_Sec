import socket
import json
import RPi.GPIO as GPIO
import time

HOST = "192.168.1.4"
PORT = 5000
PIR_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def get_pir_data():
  return GPIO.input(PIR_PIN)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  sock.connect((HOST, PORT))
  print("connect")
except ConnectionRefusedError:
  print("not connect")
  exit()

while True:
  if get_pir_data():
    message = {"message": "detect"}
    data = json.dumps(message).encode()
    sock.sendall(data)
    print("detected")
    time.sleep(1)  
  else:
 
    time.sleep(0.1)  
