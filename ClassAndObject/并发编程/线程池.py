

from socket import AF_INET,SOCK_STREAM,socket
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

#3个要素  绑定的socket(由accept生成)、分配的线程(由ThreadPoolExecutor来)、任务代码(想该连接执行什么任务)
#用浏览器来测试该server,发现每个过来的请求都对应唯一的端口，岂不是说一个ip最多就能对该server发送65536个请求，
#那测试那边的单机十万乃至百万请求压力测试是怎么造的？变换ip?原来是加网卡即2块网卡就能模拟10w请求

#当创建一个线程时，操作系统会预留一个虚拟内存区域来放置线程的执行栈(通常8MB)。但这个虚拟内存只有一小片段被实际
#映射到真实内存中。所以进程中使用到的真实内存其实很小(比如200个线程理论是9GB，但其实只用了70MB的真实内存)。可用
#threading.stack_size()函数来降低。



#ThreadPoolExecutor 自动线程池(相对手动自创好处是 可方便获取返回值)，有复用机制，随机从池中取用线程
def echo_handle(sock,client_addr):
    print('Got connection from',client_addr)
    print('current thread is ',threading.current_thread().name)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')
    sock.close()

def echo_server(addr):#每一个请求都将建立一个连接，随后只需将绑定的 sock 分配到 某个线程 中放入 任务代码 中执行即可
    pool = ThreadPoolExecutor(128)
    sock = socket(AF_INET,SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock,client_addr = sock.accept()#数据就绪(即到了内核态)同时将会生成一个新的socket与对端绑定后交给线程池
        a = pool.submit(echo_handle,client_sock,client_addr)#线程池将绑定的socket与绑定信息作为参数传给处理单元(或函数或类)
        #并选定池中的一个线程开始执行，当任务执行完成后将会把该线程放回线程池中

        # x = a.result()#可拿到对应线程完成的结果，若结果还没拿到将会阻塞
        # a.add_done_callback()#若不想等待结果时阻塞，则使用回到函数


#手动queue自创线程池(线程执行完后，没有复用机制，致线程成为了一次性资源，需要自己造)
def echo_handle_hand(q):
    sock,client_addr = q.get()#q为队列，里面装着元组集，(绑定的sock,对端地址)
    print('Got connection from',client_addr)
    print('current thread is ', threading.current_thread().name)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print('Client closed connection')

def echo_server_hand(addr,nworkers):
    q = Queue()
    for n in range(nworkers):
        t = threading.Thread(target=echo_handle_hand,args=(q,))#将所有的线程 都共享 队列q，可随时从中提取元组数据
        t.daemon =True#主线程一直在while True，所以子线程将一直在后台监听队列 q，当有数据时就拿出来，没有就阻塞
        t.start()

    sock = socket(AF_INET,SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:#缺点是提交给线程执行后，对于执行后的结果无法掌控，需要自己定制
        client_sock,client_addr = sock.accept()
        q.put((client_sock,client_addr))



if __name__ == '__main__':
    echo_server_hand(('',15000),12)