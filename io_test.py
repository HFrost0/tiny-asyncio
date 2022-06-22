import socket

import taio


async def main():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setblocking(False)
    loop = taio.get_event_loop()
    await loop.sock_connect(sock, ('127.0.0.1', 6666))
    sock.send(b'hey server, Im taio')
    data = await loop.sock_recv(sock, 1024)
    print(data)
    sock.close()


if __name__ == '__main__':
    loop = taio.get_event_loop()
    loop.create_task(main())
    loop.create_task(main())
    loop.create_task(main())
    loop.create_task(main())
    loop.create_task(main())
    loop.call_later(1.5, loop.stop)
    loop.run_forever()
