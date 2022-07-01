import random
import socket
import time
from concurrent.futures import ThreadPoolExecutor


def accept(s: socket.socket):
    while True:
        data = s.recv(1024)
        if data:
            # time.sleep(1)  # slow down respond
            s.send(data)
            print(f'Echo: {data}')
        else:
            print(f'Remove: {s}')
            break


if __name__ == '__main__':
    pool = ThreadPoolExecutor()
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', 6666))
    server_sock.listen()
    while True:
        s, addr = server_sock.accept()
        print(f'Connection: {addr}')
        pool.submit(accept, s)
