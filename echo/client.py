import socket

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 6666))
    s.sendall(b'hello server Im client')
    data = s.recv(1024)
    print(data)
