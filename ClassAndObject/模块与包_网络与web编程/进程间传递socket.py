
from multiprocessing.reduction import recv_handle,send_handle

import multiprocessing
import socket


#缺陷在于管道只能在同一台 机器上进行相互 读取与写入，所以可以用分布式进程来优化
#实现方式就在于send_handle函数是用哪种连接作为发送文件描述符，若用管道则是本机的，若用socket则是分布式进程

def worker(in_p,out_p):
    out_p.close()#关闭写入，仅读取
    while True:
        fd = recv_handle(in_p)#从管道中拿取 socket的文件描述符
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

def server(address,in_p,out_p,worker_pid):
    in_p.close()#关闭读取，仅写入
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)#表明该socket为可重用socket，即可生成新的sokcet
    s.bind(address)
    s.listen(1)
    print("监听port %s ..."%(address[1]))
    while True:
        # accept将返回一个表示连接的新 socket以及对应客户端的地址信息，即用新的socket与该客户端建立连接，所以本
        # socket继续监听。新socket的文件描述符被传入到对应进程的管道中
        client,addr = s.accept()
        print("client: ")
        print(client)
        print('SERVER: Got connection from',addr)
        print('server中新建的fd号',client.fileno(),s.fileno())
        send_handle(out_p,client.fileno(),worker_pid)#将 客户端文件描述符，工作进程id 写入管道即进行派遣
        #很关键的一点，send 的 fd 和 recv 的 fd 不一定一样，而且基本上都不一样！因为在内核中将会有一次复制该描述符
        client.close()

if __name__ == '__main__':
    c1,c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=worker,args=(c1,c2))
    worker_p.start()
    server_p = multiprocessing.Process(target=server,args=(('',15000),c1,c2,worker_p.pid))
    server_p.start()
    # c1.close()
    # c2.close()