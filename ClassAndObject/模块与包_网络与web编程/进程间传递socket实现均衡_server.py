
from multiprocessing.reduction import recv_handle,send_handle
from multiprocessing.connection import Listener

import multiprocessing
import socket


def server(work_address,port):

    work_serv = Listener(work_address,authkey=b'peekaboo')
    worker = work_serv.accept()
    worker_pid = worker.recv()#当前只能注册一个worker，改成多个的逻辑只需将多个worker的pid拿到进行轮询分发即可，

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)#表明该socket为可重用socket，即可生成新的sokcet
    s.bind(('',port))
    s.listen(1)
    print("监听port %s ..."%port)
    while True:
        # accept将返回一个表示连接的新 socket以及对应客户端的地址信息，即用新的socket与该客户端建立连接，所以本
        # socket继续监听。新socket的文件描述符被传入到对应进程的管道中
        client,addr = s.accept()
        print("client: ")
        print(client)
        print('SERVER: Got connection from',addr)
        print('server中新建的fd号',client.fileno(),s.fileno())
        send_handle(worker,client.fileno(),worker_pid)#将 客户端文件描述符，工作进程id 写入到worker中即一个socket中
        #send_handle(conn, handle, destination_pid)
        #conn(multiprocessing.Connection)：示通过其发送文件描述符的连接(可以是管道、socket等)
        #handle(int)：整数，表示文件描述符 / 句柄
        #destination_pid(int)：接收文件描述符的进程的整数 pid - 当前仅在 Windows 上使用

        client.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) !=3:
        print('Usage: server.py server_address port',file=sys.stderr)
        raise SystemExit(1)
    server(sys.argv[1],int(sys.argv[2]))