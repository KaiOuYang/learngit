
import socket

def client(addr):
    client = socket.socket()
    client.connect(addr)
    # while True:
    client.send(b'Hello')
    data = client.recv(1024)
    print(client.fileno(),' ',data)


if __name__ == '__main__':
    addr = ('127.0.0.1',8080)
    client = socket.socket()
    client.connect(addr)
    print('client建立连接')

    client2 = socket.socket()
    client2.connect(addr)
    print('client2建立连接')

    client.send(b'Hello')
    data = client.recv(1024)
    print('client发送数据')
    print(client.fileno(),' ',data)

    client2.send(b'Hello')
    data = client2.recv(1024)
    print('client2发送数据')
    print(client2.fileno(),' ',data)

