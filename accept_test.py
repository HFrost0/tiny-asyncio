import socket

import taio


async def accept():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.bind(('', 6666))
    sock.listen()
    loop = taio.get_event_loop()
    conn, address = await loop.sock_accept(sock)
    data = await loop.sock_recv(conn, 1024)
    print(f'Echo: {data}')
    conn.send(data)


if __name__ == '__main__':
    loop = taio.get_event_loop()
    loop.run_until_complete(accept())
