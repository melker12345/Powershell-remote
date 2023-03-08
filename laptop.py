import socket

HOST = '192.168.1.201' # Replace with the IP address of your Windows PC
PORT = 42069          # Replace with the port number you chose

s = socket.socket()
s.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

while True:
    command = input("> ")
    if command.lower() == 'exit':
        break

    s.sendall(command.encode())
    output = s.recv(4096).decode()
    print(output.strip())

s.close()