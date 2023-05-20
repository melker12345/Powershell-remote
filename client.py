import socket

HOST = '192.168.1.201'  # Replace with the IP address of your Windows PC
PORT = 8888             # Replace with the port number you chose

command_history = []

conn = socket.socket()
conn.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

while True:
    command = input("> ")
    if not command:
        print(f"{command} Not valid!")
        continue
    if command.lower() == 'q!':
        conn.close()
        break

    if command == '!!':  # Execute the previous command
        if command_history:
            command = command_history[-1]
        else:
            print("No previous command in history")
            continue

    # Add command to history
    command_history.append(command)

    conn.sendall(command.encode())
    output = conn.recv(8200).decode()
    print(output.strip())

conn.close()
