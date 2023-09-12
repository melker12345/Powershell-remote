import socket
import subprocess
import os

HOST = '10.10.1.1'  # Listen on all network interfaces
PORT = 8080  # Choose a port number


s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT}")

while True:
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    while True:
        # Receive command from the client
        command = conn.recv(8192).decode().strip()

        if not command:
            print(f"{command} Is not a command!")
            break

        if command == "q!" or command == "Q!":  # Fix condition for termination
            conn.close()
            break

        # Split command and arguments
        cmd_parts = command.split()
        cmd = cmd_parts[0]
        args = cmd_parts[1:]

        if cmd == "cd":
            try:
                os.chdir(args[0])
                # Get the current working directory
                current_dir = os.getcwd()
                response = f"\nChange to:\n{current_dir}\n"
                conn.sendall(response.encode())
            except Exception as e:
                conn.sendall(str(e).encode())

        if cmd.startswith('git'):
            try:
                # Execute Git command using subprocess.run
                git_command = ['git'] + cmd_parts[1:]
                process = subprocess.run(
                    git_command,
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd(),
                    shell=True)

                # Get the command output and return code
                output = process.stdout.strip()
                return_code = process.returncode

                # Send the output and return code back to the client
                response = output.encode() + b'\nReturn Code: ' + str(return_code).encode()
                conn.sendall(response)
            except Exception as e:
                conn.sendall(str(e).encode())
        else:
            try:
                # Execute PowerShell command using subprocess.run
                powershell_command = ['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command]
                process = subprocess.run(
                    powershell_command,
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd(),
                    shell=True  # Add shell=True for executing PowerShell commands
                )

                # Get the command output and return code
                output = process.stdout.strip()
                return_code = process.returncode

                # Send the output and return code back to the client
                response = output.encode() + b'\nReturn Code: ' + str(return_code).encode()
                conn.sendall(response)
            except Exception as e:
                conn.sendall(str(e).encode())

    conn.close()
    if input(">") == "q!":
        s.close()
        break
