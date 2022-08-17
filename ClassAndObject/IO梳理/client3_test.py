import socket


def client(addr):
    client = socket.socket()
    client.connect(addr)
    # while True:
    client.send(b'Hello')
    data = client.recv(1024)
    print(client.fileno(), ' ', data)


def bioThreadsClient():
    addr = ('127.0.0.1', 8080)
    client = socket.socket()
    client.connect(addr)
    print('client2建立连接')

    while True:
        client.send(b'Hello2')
        client.send(b'world2')
        client.send(b'lady2')
        client.send(b'gaga2')
        data = client.recv(1024)
        print('client2发送数据')
        print(client.fileno(), ' ', data)

        import time
        print("休眠3秒")
        time.sleep(3)


def nbioThreadsClient():
    addr = ('127.0.0.1', 8081)
    client = socket.socket()
    client.connect(addr)
    print('client建立连接')

    while True:
        client.send(b'Hello')
        client.send(b'world')
        client.send(b'lady')
        client.send(b'gaga')
        data = client.recv(1024)
        print('client发送数据')
        print(client.fileno(), ' ', data)


if __name__ == '__main__':
    bioThreadsClient()
    # nbioThreadsClient()

