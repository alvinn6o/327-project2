# TCP server for anycast simulation
# Each server instance responds with a unique greeting based on SERVER_NAME env var

import socket
import os

HOST = '0.0.0.0'  # listen on all interfaces
PORT = 5000

# each server container gets a unique name via environment variable
SERVER_NAME = os.environ.get('SERVER_NAME', 'server')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket

s.bind((HOST, PORT))
s.listen(5)

print(f'Server ready on port {PORT}')

while True:
    # accept a client connection
    client_socket, client_addr = s.accept()
    print(f'Connection from {client_addr}')

    # send greeting from server
    message = f'Hello from {SERVER_NAME}'
    client_socket.send(message.encode('utf-8'))
    print(f'Sent: {message}')
    client_socket.close()
