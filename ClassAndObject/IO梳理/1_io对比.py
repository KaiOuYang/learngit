

import socket,time


'''
当我们创建一个 socket 监听某个端口后，所有完成三次握手的客户端连接，都会按照到达先后顺序被放入主线 socket 的等待连接队列中。先放入的先被取出
当 socket 执行 listen() 后，可以调用 accept() 函数从等待连接队列中取出一个连接请求，并创建一个新的 socket 用于与客户端通信，然后返回。
阻塞模式下，主线 socket 调用 accept 后，如果等待队列中没有新的请求，就会一直阻塞，直到可以从队列中取出新的请求才返回。
非租塞模式下，如果等待队列中没有可取的连接，accept() 也会立马返回，并抛出 BlockingIOError: [Errno 11] Resource temporarily unavailable 异常。
此时，我理解的资源不可用，是指等待连接队列中没有数据可取！
可以触发 EAGAIN 错误的操作有：accept()、recv()、send()。
原文链接：https://blog.csdn.net/pythontide/article/details/109242386
'''


def bio_test():
    server = socket.socket()
    addr = ('127.0.0.1',8080)
    server.bind(addr)
    print('listen...',addr)
    server.listen(5)

    while True:#server准备接收多个请求(建立多个连接)，请求执行时顺序执行，上一个请求完成后，下一个才能建立连接并执行
        conn,addr = server.accept()#新建立socket连接，可以如同nbio一样建立多个连接，直至等待队列为空
        print('接收到连接 ',addr)
        while True:#每个连接多次互动收发数据
            try:
                data = conn.recv(1024)#recvfrom系统调用
                if len(data) == 0:
                    break
                print('server recv data: ',data)
                conn.send(data.upper())
                print("延时1秒")
                time.sleep(1)
            except ConnectionResetError as e:
                break
        conn.close()


def bioMixNo_test():#
    '''
    阻塞型IO可以用轮询的方式，但比较迂回。因为非阻塞型IO执行accept时将从等待连接队列中拿取连接请求，依据该请求
    创建新的socket用于和客户端通信，然后返回形成conn与addr，当等待连接队列为空时会非阻塞型IO将抛出BlockingIOError
    表明连接都已建立，故可依据此Error开始轮询各个连接。但阻塞型IO执行accept时若等待队列没有请求了，将会一直堵塞，直到
    可以从队列中取出新的请求才返回。
    所以要想 轮询+阻塞型IO，则需要方法提前判断等待队列中是否为空，当为空时就不执行accept而是直接开始轮询。

    '''
    server = socket.socket()
    addr = ('127.0.0.1',8080)
    server.bind(addr)
    print('listen...',addr)
    server.listen(5)

    r_list = []
    del_list =[]

    while True:#多个请求都建立了连接，请求执行时交错进行
        try:
            conn,addr = server.accept()
            print('接收到连接 ', addr)
            r_list.append(conn)
        except IOError:
            for conn in r_list:
                try:
                    data = conn.recv(1024)  # recvfrom系统调用
                    if len(data) == 0:
                        break
                    print('server recv data: ', data)
                    conn.send(data.upper())
                    print("延时1秒")
                    time.sleep(1)
                except ConnectionResetError as e:
                    break


def nbio_test():
    server = socket.socket()
    addr = ('127.0.0.1', 8081)
    server.bind(addr)
    print('listen...', addr)
    server.listen(5)
    server.setblocking(False)

    r_list = []
    del_list =[]
    while True:#多个请求都建立了连接，请求执行时交错进行
        try:
            conn,addr = server.accept()
            print('接收到连接 ', addr)
            r_list.append(conn)
        except BlockingIOError:
            for conn in r_list:
                try:
                    data = conn.recv(1024)
                    if len(data) == 0:
                        conn.close()
                        del_list.append(conn)
                        continue
                    conn.send(data.upper())
                    print("延时1秒")
                    time.sleep(1)
                except BlockingIOError:
                    print(conn.fileno(),"数据未就绪")
                    continue
                except ConnectionResetError:
                    conn.close()
                    del_list.append(conn)
            for conn in del_list:
                r_list.remove(conn)
            del_list.clear()


def mio_test():#IO复用指的是s端的监控线程是被复用的,多路复用使用的可以是非阻塞型(常用)也可以阻塞型，表明多路复用只是一种监控机制
    import select
    server = socket.socket()
    addr = ('127.0.0.1', 8082)
    print('listen...', addr)
    server.bind(addr)
    server.listen(5)
    server.setblocking(False)
    read_list = [server]

    while True:
        r_list,w_list,xlist = select.select(read_list,[],[])#帮忙监管 各对象对应的IO是否数据就绪，有则返回，无则堵塞
        for i in r_list:
            if i is server:
                conn,addr = i.accept()
                read_list.append(conn)
            else:
                res = i.recv(1024)
                if len(res) == 0:
                    read_list.remove(i)
                    continue
                print(res)
                i.send(b'hahahhaahahah')


def client(addr):
    import socket
    client = socket.socket()
    client.connect(addr)
    while True:
        client.send(b'Hello')
        data = client.recv(1024)
        print(data)

if __name__ == '__main__':
    # bio_test()
    # nbio_test()
    bioMixNo_test()

