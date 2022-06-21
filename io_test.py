import socket

import taio


async def main():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setblocking(False)
    loop = taio.get_event_loop()
    await loop.sock_connect(sock, ('127.0.0.1', 6666))
    # sock.send(b'what')  # todo this line will cause ConnectionResetError in server side due to no blocking
    return sock


if __name__ == '__main__':
    loop = taio.get_event_loop()
    sock = loop.run_until_complete(main())
    print(sock)
