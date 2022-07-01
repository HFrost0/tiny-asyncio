import random
import socket

# import asyncio as taio
import taio


async def client(message):
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setblocking(False)
    loop = taio.get_event_loop()

    # await loop.sock_connect(sock, ('127.0.0.1', 6666))
    # sock.send(message)
    # data = await loop.sock_recv(sock, 1024)

    try:
        # await taio.sleep(random.random())
        await loop.sock_connect(sock, ('127.0.0.1', 6666))
        sock.send(message)
        data = await loop.sock_recv(sock, 1024)
    except Exception as e:
        # if str(e) == '[Errno 32] Broken pipe':
        #     raise
        print(e)
        sock.close()
        return

    print(data)
    sock.close()
    return data


async def main():
    cors = []
    for i in range(150):
        cors.append(client(f'{i} taio client'.encode('utf8')))
    datas = await taio.gather(*cors)
    print('All: ', datas)


if __name__ == '__main__':
    loop = taio.get_event_loop()
    loop.run_until_complete(main())
