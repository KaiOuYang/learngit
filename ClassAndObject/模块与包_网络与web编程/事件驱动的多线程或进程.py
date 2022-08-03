

from concurrent.futures import ThreadPoolExecutor

import os,socket,select


def eventloop(handlers):
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive]
        wants_send = [h for h in handlers if h.wants_to_send]
        recvs,sends,_ = select.select(wants_recv,wants_send,[])
        for r in recvs:
            r.handle_receive()
        for s in sends:
            s.handle_send()

class EventHandler:

    def fileno(self):
        raise NotImplemented("must be implemented.")

    def wants_to_receive(self):
        return False

    def wants_to_send(self):
        return False

    def handle_receive(self):
        pass

    def handle_send(self):
        pass

class ThreadPoolHandler(EventHandler):

    def __init__(self,nworkers):#创出2个socket，1个signal_done_sock，1个done_sock
        if os.name == 'posix':
            self.signal_done_sock,self.done_sock = socket.socketpair()#创建一对无名的，相互连接的套接字
            #这对套接字可以全双工通信及任意一个都可读可写
            #socketpair创建的套接字组，只适用于父子进程或线程间通信，若想实现任意2个进程间的双向通信，则需要将socketpair
            #创建的一个描述符fd发送给另一个进程，相当于两个不同的进程访问同一个文件。
        else:
            #出现3个socket。首先创建2个socket，一个是server用于本地监听端口，一个是signal_done_sock
            #然后将signal_done_sock与server进行connect，即设置signal_done_sock的对端就是server的address，
            #因server先前已经在监听状态，故signal_done_sock的连接请求将会回应，即server.accept将会产生一个新
            #的socket即done_sock，该socket的本端addr脱胎于server故与server一样，对端addr即为signal_done_sock的地址
            #由此将signal_done_sock与done_sock建立了全双工连接。最后将server关闭。
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server.bind(('127.0.0.1',0))
            server.listen(1)
            self.signal_done_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            # getsockname返回address info，即创建了新socket为signal_done_sock，将该socket与server互联
            #形成一组套接字
            self.signal_done_sock.connect(server.getsockname())
            #server.accept返回了1个新的socket即done_sock与client的address info，该socket与client建立了连接
            #而这个client就是 signal_done_sock，因为前面一步 signal_done_sock对server进行了连接，此时server接受了
            self.done_sock,_ = server.accept()
            #所以signal_done_sock与done_sock进行了互联
            server.close()

        self.pending = []
        self.pool = ThreadPoolExecutor(nworkers)

    def fileno(self):
        return self.done_sock.fileno()

    def _complete(self,callback,r):
        self.pending.append((callback,r.result()))
        self.signal_done_sock.send(b'x')

    def run(self,func,args=(),kwargs={},*,callback):
        #submit后返回的是一个期物r,当该期物完成后，将会事件通知由add_done_callback提交的对应回调函数
        r = self.pool.submit(func,*args,**kwargs)
        r.add_done_callback(lambda r:self._complete(callback,r))#为何要将回调放置到_complete进行包裹呢?
        #因为任务提交给pool后将会返回一个期物，随后给该期物添加上对应的完成后事件通知 回调函数(此处的回调是匿名函数，
        # 包裹了任务对应的回调函数)，当任务完成将会触发该匿名函数执行，则将执行 _complete函数将任务对应的回调函数和
        #期物本身添加到ThreadPoolHandler实例中数组内，并由signal_done_sock向done_sock发送信号
        #而done_sock本身是受到事件循环eventloop的select监测的，所以当有请求到达done_sock时，事件循环将运行
        #然后执行ThreadPoolHandler实例的handle_receive，将pending中的任务对应的回调函数与期物结果结合执行
        #每轮执行完毕都清理一遍pending列表。

        #就是说，不管handlers列表中有多少服务器，各个服务器每接到一个客户端请求都会将对应的任务、参数、回调函数交给
        #ThreadPoolHandler实例内的线程池pool，每个请求都生成一个期物，并给该期物添加上当期物完成后事件通知的回调函数即
        #此处是一个匿名函数，该匿名函数嵌套了_complete函数该函数用于将任务对应的回调函数和期物本身添加到
        #ThreadPoolHandler实例内的pending列表中，随后发送信号到受到事件循环监测的done_sock，使得
        #循环继续进行，则ThreadPoolHandler实例对应的handle_receive将执行将pending中积攒的任务对应的回调函数和期物本身
        #结合执行。
        # 至于pending中有多少组，取决于各个期物完成的时间，因为是在期物完成后触发事件通知调用回调才会将任务回调函数于期物本身
        #放置到pending中(所以会不会有线程不安全事项？因pending是共享的，会有，但也确实解决了事件循环被堵塞的瓶颈)

    def wants_to_receive(self):
        return True

    def handle_receive(self):
        for callback,result in self.pending:
            callback(result)
            self.done_sock.recv(1)
        self.pending = []


def fib(n):
    if n <2:
        return 1
    else:
        return fib(n-1) + fib(n -2)



class UDPServer(EventHandler):#服务器类负责 具体配置不同类型的服务器
    def __init__(self,address):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind(address)

    def fileno(self):#select将调用该函数来监听是否有数据到达
        return self.sock.fileno()

    # def wants_to_send(self):
    #     return True

    def wants_to_receive(self):
        return True

class UDPFibServer(UDPServer):
    def handle_receive(self):
        #在event里循环等待客户端请求到来后，将会被event调用handle_receive，将到来的数据和任务以及任务完成后的回调动作都交给
        #线程池来处理，就不用管随后的事了，线程池分配的线程将会在完成任务后将执行回调函数将结果告知 对应的客户端。
        msg,addr = self.sock.recvfrom(128)
        n = int(msg)
        pool.run(fib,(n,),callback=lambda r:self.respond(r,addr))

    def respond(self,result,addr):
        self.sock.sendto(str(result).encode('ascii'),addr)


if __name__ == '__main__':
    pool = ThreadPoolHandler(16)
    handlers = [pool,UDPFibServer(('',16000))]
    eventloop(handlers)