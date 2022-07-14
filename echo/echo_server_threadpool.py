import socket
from concurrent.futures import ThreadPoolExecutor


def accept(s: socket.socket):
    while data := s.recv(1024):
        s.send(data)
        # sum(range(100000))  # slow down respond
        print(f'Echo: {data}')
    s.close()
    print(f'Remove: {s}')


if __name__ == '__main__':
    pool = ThreadPoolExecutor()
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', 6666))
    server_sock.listen()
    while True:
        s, addr = server_sock.accept()
        print(f'Connection: {addr}')
        pool.submit(accept, s)
