import socket
import selectors


def accept_connect(server: socket.socket, sel: selectors.DefaultSelector):
    client, addr = server.accept()
    client.setblocking(False)
    sel.register(client.fileno(), selectors.EVENT_READ, data=(echo, client, sel))


def echo(sock: socket.socket, sel: selectors.DefaultSelector):
    data = sock.recv(1024)
    if data:
        print(f'Echo: {data}')
        sock.send(data)  # echo back
    else:
        print(f'Remove: {sock}')
        sel.unregister(sock.fileno())
        sock.close()


def startup_server(ip, port):
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.bind((ip, port))
    server.setblocking(False)
    server.listen()

    sel = selectors.DefaultSelector()
    sel.register(server.fileno(), selectors.EVENT_READ, data=(accept_connect, server, sel))
    while True:
        event_list = sel.select()
        for key, mask in event_list:
            # fileobj, (reader, writer) = key.fileobj, key.data
            cb, *args = key.data
            cb(*args)


if __name__ == '__main__':
    startup_server('', 6666)
