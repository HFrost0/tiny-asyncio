"""
DO NOT use this server for c10k test!
"""
import random
import socket
import time
import threading


def accept(s: socket.socket):
    while data := s.recv(1024):
        # time.sleep(1)  # slow down respond
        s.send(data)
        print(f'Echo: {data}')
    s.close()
    print(f'Remove: {s}')


if __name__ == '__main__':
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', 6666))
    server_sock.listen()
    threads = []
    while True:
        s, addr = server_sock.accept()
        print(f'Connection: {addr}')
        t = threading.Thread(target=accept, args=(s, ))
        threads.append(t)
        t.start()
