# This is the sever/host script

import socket

HOST = '192.168.1.120' # Enter your ip address
PORT = 42069   # Enter port number

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print(f"[*] Listening on {HOST}:{PORT}")

conn, addr = s.accept()
print(f"[*] Connection from {addr[0]}:{addr[1]}")

while True:
    command = input('Enter command: ')
    conn.sendall(command.encode())
    if command.lower() == 'exit':
        conn.close()
        break
    result = conn.recv(1024).decode()
    print(result)

s.close()
