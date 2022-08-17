


import socket,time,threading
from concurrent.futures import ThreadPoolExecutor


import time


'''
1. accept产生的socket都是阻塞型的
2. 数据复制阶段是要占用cpu的

3.阻塞型IO：
  单线程中，阻塞型IO例子中server的socket是阻塞型，每个请求严格顺序执行完成
  多线程中，server的socket是阻塞型，accept生成的socket均是阻塞型
  非阻塞型IO:
  单线程中，阻塞型IO例子中server的socket是非阻塞型，所以可以由列表收集，从而轮询，相交执行各个请求
  多线程中，server的socket是，accept生成的socket均是阻塞型
  
  因为数据就绪阶段由select接管了，所以阻塞与非阻塞在这个阶段一致了，而
  在数据复制阶段两种类型的IO都是需要cpu介入的。
因为若产生的是非阻塞型的io则切换到子线程时，将子线程一直执行到结束而主线程拿不到cpu。

'''

#阻塞型IO 线程任务
def bioTask(conn,addr):
    print('Got connection from',addr)
    print('current thread is ',threading.current_thread().name)
    while True:
        try:  # 2种断开连接方式，一是正常断开即发来的数据为空、二是强制断开
            data = conn.recv(1024)
            if len(data) == 0:
                break
            conn.send(data.upper())
            print('current thread is ', threading.current_thread().name,'休眠3秒')
            time.sleep(3)
        except ConnectionResetError as e:  # 远程主机强制关闭现有连接错误
            break
    conn.close()

#阻塞型IO 线程池
def bioThreadsTest():
    server = socket.socket()
    address = ('127.0.0.1',8080)
    print('listen...', address)
    server.bind(address)
    server.listen(5)

    pool = ThreadPoolExecutor(8)
    while True:
        conn,addr = server.accept()#阻塞型IO会因为 等待队列无请求而阻塞
        spaceResult = pool.submit(bioTask,conn,addr)
        i = 0
        while True:
            i += 1
            print(threading.current_thread().name,"主线程占用了cpu执行中...",i)

#非阻塞型IO 线程任务
def nbioTask(conn,addr):
    print('Got connection from',addr)
    print('current thread is ',threading.current_thread().name)
    conn.setblocking(False)#设置为非阻塞io 是否生效？会生效！若生效则cpu会在数据就绪阶段一直在该子线程中而不是切换回主线程，除非时间片耗尽
    while True:
        try:  # 2种断开连接方式，一是正常断开即发来的数据为空、二是强制断开
            data = conn.recv(1024)
            if len(data) == 0:
                break
            conn.send(data.upper())
            print('current thread is ', threading.current_thread().name,'休眠3秒')
            time.sleep(3)
        except BlockingIOError:#客户端连接上，但不发送数据即可
            print(conn.fileno(), "数据未就绪")
            continue
        except ConnectionResetError as e:  # 远程主机强制关闭现有连接错误
            break
    conn.close()


#非阻塞型IO 线程池
def nbioThreadsTest():
    server = socket.socket()
    address = ('127.0.0.1',8081)
    print('listen...', address)
    server.bind(address)
    server.listen(5)
    server.setblocking(False)

    pool = ThreadPoolExecutor(8)
    r_list = []
    del_list = []
    while True:
        try:
            conn,addr = server.accept()#非阻塞型IO会因为 等待队列无请求而一直触发 BlockingIOError
            r_list.append(conn)
        except BlockingIOError:
            for i in r_list:
                spaceResult = pool.submit(nbioTask, i, '未知')
            r_list = []
            for i in range(10):
                print(threading.current_thread().name, "主线程占用了cpu执行中...", i)




if __name__ == '__main__':
    # bioThreadsTest()
    nbioThreadsTest()
