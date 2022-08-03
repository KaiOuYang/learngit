
from functools import partial
from socket import socket,AF_INET,SOCK_STREAM

import contextlib

class LazyConnection:
    def __init__(self,address,family=AF_INET,type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.connections = []#后进先出 栈


    def __enter__(self):
        print("__enter__")
        self.sock = socket(self.family,self.type)
        self.sock.connect(self.address)
        self.connections.append(self.sock)
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connections.pop().close()
        print("exc_type:%s , exc_val:%s , exc_tb:%s" % (exc_type, exc_val, exc_tb))
        print("__exit__")
        return 8


@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write

    yield "banana"
    sys.stdout.write = original_write
    print("looking_glass_exit")




if __name__ == '__main__':
    conn = LazyConnection(('localhost',8888))
    conn2 = LazyConnection(('localhost',8888))
    try:
        with conn as s:
            s.send(b'GET /tree HTTP/1.0\r\n')
            s.send(b'Host: localhost\r\n')
            s.send(b'\r\n')
            resp = b''.join(iter(partial(s.recv,8192),b''))
            raise ValueError("bad value")
            print(resp)
    except:
        print("外层ValueError:")


    with  looking_glass() as f:
        print(f)
        raise ValueError("f error")
