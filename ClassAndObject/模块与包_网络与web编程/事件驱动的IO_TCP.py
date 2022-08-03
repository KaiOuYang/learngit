import select,socket,time


#所有的事件驱动框架原理与下述相差无几，在最核心的地方都会有一个轮询的循环来检查活动socket
#并执行响应操作。
#事件驱动IO好处是能处理非常大的并发连接，而不需要多线程或进程。即select能监听大量的socket并
#响应它们中任何一个事件。在循环一次处理一个事件，并不需要其他并发机制。
#缺点是若 事件处理器方法(即回调函数)阻塞或耗时计算，就会阻塞所有处理进程。且调用不是事件驱动
#风格的库函数也会有问题，若阻塞也会导致整个事件循环停止。

#所以对于 阻塞或耗时计算的问题可通过将事件发送到其他单独的进程或现场进行处理。这就涉及到多线程或
#多进程，不过在事件循环中引入多线程或进程比较棘手(见cookbook 11.12 是 reactor类网络编程模型的雏形)

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


class TCPServer(EventHandler):

    def __init__(self,addr,client_handler,handler_list):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
        self.sock.bind(addr)
        self.sock.listen(1)
        self.client_handler = client_handler
        self.handler_list = handler_list

    def fileno(self):
        return self.sock.fileno()

    def wants_to_receive(self):
        return True


    def handle_receive(self):#数据就绪后即select放行后才会调用该  回调函数
        client,addr = self.sock.accept()
        self.handler_list.append(self.client_handler(client,self.handler_list))
        #服务器与客户端都有 handler_list的引用，便于从处理器列表中增加和删除客户端，对于每一个连接
        #一个新的处理器被创建并加到列表。本质是由于客户端与 服务器都写在一起了，所以才会有如此操作，
        # 即同一个 eventloops处理相互联通的 server与client


class TCPClient(EventHandler):
    def __init__(self,sock,handler_list):
        self.sock = sock
        self.handler_list = handler_list
        self.outgoing = bytearray()

    def fileno(self):
        return self.sock.fileno()

    def close(self):
        self.sock.close()
        self.handler_list.remove(self)


    def wants_to_send(self):
        return True if self.outgoing else False

    def handle_send(self):
        nsent = self.sock.send(self.outgoing)
        self.outgoing = self.outgoing[nsent:]


class TCPEchoClient(TCPClient):
    def wants_to_receive(self):
        return True

    def handle_receive(self):
        data = self.sock.recv(8192)
        if not data:
            self.close()
        else:
            self.outgoing.extend(data)



if __name__ == '__main__':
    handlers = []
    handlers.append(TCPServer(('',16000),TCPEchoClient,handlers))
    eventloop(handlers)