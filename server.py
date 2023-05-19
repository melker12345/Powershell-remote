import socket
import subprocess
import os

HOST = '192.168.1.201'  # Listen on all network interfaces
PORT = 8888  # Choose a port number

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT}")

while True:
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    while True:
        # Receive command from the client
        command = conn.recv(4096).decode().strip()

        if not command:
            print(f"{command} Is not a command!")
            break

        if command == "q!":
            conn.close()
            break

        # Split command and arguments
        cmd_parts = command.split()
        cmd = cmd_parts[0]
        args = cmd_parts[1:]

        if cmd.startswith('git'):
            try:
                # Execute Git command directly
                git_command = ['git'] + cmd_parts[1:]
                process = subprocess.Popen(
                    git_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=os.getcwd()
                )

                # Read the output of the Git command
                output = process.communicate()[0]

                # Send the output back to the client
                conn.sendall(output)
            except Exception as e:
                conn.sendall(str(e).encode())
        else:
            try:
                # Execute PowerShell command
                powershell_command = ['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive', '-Command', command]
                process = subprocess.Popen(
                    powershell_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=os.getcwd()
                )

                # Read the output of the PowerShell command
                output = process.communicate()[0]

                # Send the output back to the client
                conn.sendall(output)
            except Exception as e:
                conn.sendall(str(e).encode())

    conn.close()
    if input(">") == "q!":
        s.close()
        break
