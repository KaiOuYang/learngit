

import socket,threading
import select
from concurrent.futures import ThreadPoolExecutor


'''
https://www.cnblogs.com/tiancai/p/15983644.html
https://zhuanlan.zhihu.com/p/406293032
'''

def multiTask(conn,addr):#需要处理连接而不是单单请求
    print('Got connection from', addr)
    print('current thread is ',threading.current_thread().name)
    while True:#每个连接都是视为长连接故死循环等待数据到来，只是当缓冲区的数据都提取完成后再被阻塞后切回主线程
        try:
            data = conn.recv(1024)
            if len(data) == 0:
                break
            conn.send(b'bliblibliblin')
        except ConnectionResetError as e:
            break
    conn.close()

def multiRepeatBio():
    '''
    以前s端只有线程池时，来一个请求就即刻派一个线程从数据还未就绪时就服务对应的请求，
    多路复用则是s端先只用同一个线程来集中管理来的请求，待这些请求已经数据就绪了，再交给
    线程池派遣线程去处理。

    io多路复用与线程池可认为是并列的概念
    1.io多路复用一般还是配合单进线程
    2.io多路复用 + 线程池有多种配合方法，一是先开启多个线程池，在每个线程中都通过io多路复用的方式处理多个socket
      二是先io多路复用后，将请求交给线程池去处理，再将结果返回io多路复用
    :return:
    '''
    server = socket.socket()
    address = ('127.0.0.1',8080)
    server.bind(address)
    print('listen...', address)
    server.listen(5)
    sList=[]
    sList.append(server)

    pool = ThreadPoolExecutor(8)
    while True:
        r_list,w_list,e_list = select.select(sList,[],[])#select监控即接管了数据就绪阶段，只把有数据就绪的连接交给线程池找线程执行。
        for rObject in r_list:
            if rObject is server:
                clientSocket,addr = server.accept()
                sList.append(clientSocket)
            else:
                result = pool.submit(multiTask,rObject,addr)#异步过程。会导致同一个连接每次发来数据就占用一个线程，即多个线程对应同一个连接，资源浪费故
                sList.remove(rObject)#需要从sList中删除掉，交给线程池后就不用管该连接了，即一连接对应一线程，而Handler则是一请求对应一线程，会将线程资源用尽，因一个连接会有很多个请求



if __name__ == '__main__':
    multiRepeatBio()