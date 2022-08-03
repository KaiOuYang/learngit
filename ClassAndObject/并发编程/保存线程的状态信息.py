

from socket import socket,AF_INET,SOCK_STREAM
from functools import partial
import threading

class LazyConnection:
    def __init__(self,address,family=AF_INET,type=SOCK_STREAM):
        self.address = address#这些实例属性 对于 不同的线程将是共享的
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.local = threading.local()

    def __enter__(self):#在不同的线程中使用
        if hasattr(self.local,'sock'):#判断本线程中是否有sock属性指向了socket
            raise RuntimeError('Already connected')
        self.local.sock = socket(self.family,self.type)
        self.local.sock.connect(self.address)
        return self.local.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.local.sock.close()
        del self.local.sock


def test(conn):
    with conn as s:#在conn中的__enter__将依据本身处于的不同线程返回各自的socket
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host: www.python.org\r\n')
        s.send(b'\r\n')
        resp = b''.join(iter(partial(s.recv,8192),b''))
    print('Got {} bytes'.format(len(resp)))

if __name__ == '__main__':
    conn = LazyConnection(('www.baidu.com',80))
    t1 = threading.Thread(target=test,args=(conn,))#同一个conn实例 在不同的线程中 threading.local将保存对应线程新建的socket
    t2 = threading.Thread(target=test,args=(conn,))#达到 一个线程一个连接，而不是之前一个实例在所有进程也只有一个连接。
    t1.start()
    t2.start()
    t1.join()
    t2.join()