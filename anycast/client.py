# TCP client for anycast
# Connects to the shared server hostname, receives greeting from the 3 servers

import socket
import os

HOST = os.environ.get('SERVER_HOST', '127.0.0.1')
PORT = 5000

# create TCP socket and connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# client will now receive the server response (should be from each)
response = s.recv(1024).decode('utf-8')
print(f'Received: {response}')

s.close()

