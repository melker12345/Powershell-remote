"""
X|Add a way to exit server script(pc.py) preferably via "q!"

O|View command history like "Set-PSReadLineOption -PredictionViewStyle ListView"
O|Reformat less like powershell
O|Fix "git add --all"  

O|Filetransfer
O|Style (profiles??)  
"""
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

        if cmd == 'cd':
            try:
                os.chdir(args[0])
                conn.sendall(b'Successfully changed directory\n')
            except Exception as e:
                conn.sendall(str(e).encode())
        elif cmd == 'git' and args == ['add', '--all']:
            try:
                # Execute "git add --all" using subprocess.Popen
                process = subprocess.Popen(
                    ['git', 'add', '--all'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=os.getcwd()  # Set the current working directory for the command
                )
                
                # Read the output of the command
                output = process.communicate()[0]

                # Send the output back to the client
                conn.sendall(output)
            except Exception as e:
                conn.sendall(str(e).encode())
        else:
            try:
                # Execute the command using subprocess.Popen
                process = subprocess.Popen(
                    ['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive', '-Command', command],
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )
                
                # Read the output of the command
                output = process.communicate()[0]

                # Send the output back to the client
                conn.sendall(output)
            except Exception as e:
                conn.sendall(str(e).encode())

    conn.close()
    if input(">") == "q!":
        s.close()
        break
