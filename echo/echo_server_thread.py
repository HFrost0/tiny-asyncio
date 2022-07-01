import random
import socket
import time
import threading


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
