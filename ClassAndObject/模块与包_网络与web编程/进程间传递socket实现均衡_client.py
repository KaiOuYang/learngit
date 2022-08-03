
from multiprocessing.connection import Client
from multiprocessing.reduction import recv_handle,send_handle
from multiprocessing.connection import Listener

import multiprocessing
import socket,os


def worker(server_address):
    #规避了管道的建立(一种优化，形成分布式进程)，通过服务器的Listener来监听连入的工作者进程，工作者进程通过Client向服务器进程注册
    serv = Client(server_address,authkey=b'peekaboo')#向服务器注册本work
    serv.send(os.getpid())#发送自己的进程id

    while True:
        fd = recv_handle(serv)#拿取 服务器进程发来的socket的文件描述符
        print('CHILD: GOT FD',fd)#需要新建一个socket才能使用进行数据搬运读取
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM,fileno=fd) as s:
            print("work中新建的socket",s)
            while True:
                msg = s.recv(1024)
                print("work中的msg: ",msg)
                if not msg:
                    break
                print('CHILD: RECV {!r}'.format(msg))
                s.send(msg)


if __name__ == '__main__':
    import sys
    if len(sys.argv) !=2:
        print('Usage: worker.py server_address port',file=sys.stderr)
        raise SystemExit(1)
    worker(sys.argv[1])