import socket, errno

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(("192.168.1.1", 65535))
except socket.error as e:
    if e.errno == errno.EADDRINUSE:
        print("Port is already in use")
    else:
        # something else raised the socket.error exception
        print(e)

s.close()