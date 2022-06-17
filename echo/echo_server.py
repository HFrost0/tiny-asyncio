import socket
import select


def startup_server(ip, port):
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.bind((ip, port))
    server.setblocking(False)
    server.listen()

    readers = [server]
    while True:
        readable, writeable, errored = select.select(readers, [], [])
        # readable, writeable, errored = select.select(readers, [], [], 0.5)  # this will run once every 0.5 sec
        for s in readable:
            if s is server:
                client, addr = s.accept()
                client.setblocking(False)
                readers.append(client)
                print(f'Connection: {addr}')
            else:  # client want to send to server
                data = s.recv(1024)
                if data:
                    print(f'Echo: {data}')
                    s.send(data)  # echo back
                else:
                    print(f'Remove: {s}')
                    s.close()
                    readers.remove(s)


if __name__ == '__main__':
    startup_server('', 6666)
