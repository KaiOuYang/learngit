from socketserver import BaseRequestHandler,StreamRequestHandler,TCPServer,ThreadingTCPServer


class EchoHandler2(StreamRequestHandler):
    '''
    服务器使用了ThreadingTCPServer，可以处理多个客户端socket，它会为每个客户端连接创建一个新的线程或进程。
    但由于没有客户端连接数量的限制，若有大量恶意连接，则会让服务器崩溃。
    所以可以使用 预先分配大小的工作线程池或进程池。但这个线程池并非复用的，即若创建了有2个线程的线程池，加上主线程
    共3个，此时只能同时处理3个客户端socket，因每个客户端到服务器端后都会绑定一个线程，当3个线程都被绑定了，则第4、5个
    客户端socket就无法被服务了。但当比如第2个客户端socket断开连接即close，则第4或5个客户端socket就能占有空闲的线程，实现
    复用。
    可缺点也是必须socket的被关闭才能实现复用线程，所以能否有更优化更效率的方法呢？提出问题，若服务器端提供给客户端socket
    的服务大部分时间为IO服务，不需占用cpu进行计算，那么是否该客户端socket需要继续占有该线程进行IO任务呢？可以释放掉该线程
    还能继续IO任务的么？应该是不可以的，即客户端socket提前释放线程。
    因为该客户端socket需要执行任务，由对应的服务端线程提供任务服务，虽然该任务基本为IO任务，但线程不能被释放，因有任务就得线程执行，
    能优化的那也只能说是可以让空闲cpu切出去执行其他线程。
    再提问，所以socket的长连接将会一直占用一个服务器端的线程?所以网络上的大部分客户端请求都为短连接？
    '''

    def handle(self):
        print('Got connection from ', self.client_address)

        for line in self.rfile:#客户端发来的二进制信息要以"\n"字符结尾以告诉self.rfile终止读取，否则self.rfile将会一直在读取。
            import time
            time.sleep(10)
            print(line)
            self.wfile.write(line)

if __name__ == '__main__':

    # serv = ThreadingTCPServer(('',20000),EchoHandler2)
    # serv.serve_forever()

    from threading import Thread

    # 该种启动方式是怎样的原理？
    #一个TcpServer本质就是在监听一个服务器端的socket，当使用线程池时，即将这个监听同一个服务器端socket
    #的操作放置到了多个线程中，当有客户端socket发起请求时，此时会有一个机制使得只有一个线程去拿到客户端的请求并处理任务，当处理完毕后，该线程
    #继续监听服务器端的socket。
    # 而这个机制最有可能就是(此为自己的推测，可调试验证) ，当有读数据请求时，将会让线程与来的客户端socket进行绑定连接，直到对应的客户端socket关闭才会解绑
    #，这种机制对于这个服务端socket而言就是一种分派，即服务端socket拥有注册的多个线程，当有请求到来，就选取空闲的线程进行执行。
    #也就是说将serv.serve_forever作为target传入线程是一种注册行为，将该线程注册到指定的服务端socket中。
    #且应该存在2个容器，一个存放空闲的线程，一个存放工作的线程，循环往复，且得一直保证线程处于激活状态。
    #参考https://blog.csdn.net/pythonputao/article/details/111313340
    #此时 服务端socket其实是一个生产者的角色，本来应该有一个线程池管理器来调度线程，但下面这种方式却是在逻辑上
    #实现了线程池管理器
    nworks = 2
    serv = TCPServer(('',20000),EchoHandler2)
    for n in range(nworks):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()#若改为t.run()，且注释掉 serv.serve_forever()则变为了只有一个线程在监听，因为t.run()在第一次循环时就开启了监听将一直在此停留，也就只有一个线程
        #而t.start()只是开启线程，并未开始执行target，待全部线程启动后再 serv.serve_forever()启动，则将是多个线程一起监听
        #若是注掉了serv.serve_forever，线程池内使用的是t.start()，则直接退出，因为没有while一直监听的逻辑执行。t.start只是开启线程而已。
    serv.serve_forever()#以上的简易线程池更详细的底层原理是怎么样的呢？