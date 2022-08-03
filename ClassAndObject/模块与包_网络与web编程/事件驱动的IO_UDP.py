import select,socket,time



def event_loop(handlers):#每个handler实例既可以是 接收 也可以是 发送
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive()]
        wants_send = [h for h in handlers if h.wants_to_send()]
        print("无数据就绪，等待...")
        #若都是 接收标志的实例，则数据未就绪时将会堵塞，若存在 发送标志的实例，则select不会阻塞，即can_send中会有实例存在并往下执行回调函数
        can_recv,can_send,_ =select.select(wants_recv,wants_send,[])#若都没就绪，则堵塞在此。
        for h in can_recv:
            print("有接收数据就绪，系统调用相关回调函数", h)
            h.handle_receive()
        for h in can_send:#一旦有发送的标志，则每次轮询，can_send中都会有实例执行回调函数
            print("有发送数据就绪，系统调用相关回调函数", h)
            h.handle_send()


#三层， 事件处理器类、服务器分类类、具体业务服务器类

class EventHandler:#事件类只管事件相关的功能，可以用在UDP类型，亦可TCP

    def fileno(self):#用于select函数检查该实例对应的socket是否就绪
        raise NotImplemented('must implement')

    def wants_to_receive(self):#标明本实例对应的socket将接收数据，设置为True时，待数据就绪将 调用对应回调函数
        return False

    def handle_receive(self):#当该socket有设定 接收数据时，当数据就绪时调用本函数，即作为回调函数
        pass

    def wants_to_send(self):#标明本实例对应的socket将发送数据，设置为True时，待数据就绪将 调用对应回调函数
        return False

    def handle_send(self):#当该socket有设定 发送数据时，当数据就绪时调用本函数，即作为回调函数
        pass


class UDPServer(EventHandler):#服务器类负责 具体配置不同类型的服务器
    def __init__(self,address):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind(address)

    def fileno(self):
        return self.sock.fileno()

    # def wants_to_send(self):
    #     return True

    def wants_to_receive(self):
        return True


class UDPTimeServer(UDPServer):#具体到业务，则只需要填入 相应的回调函数即可
    def handle_receive(self):
        msg,addr = self.sock.recvfrom(125)#若只是设置为1 则缓冲区设置太小接受不了数据
        self.sock.sendto(time.ctime().encode('ascii'),addr)


    def handle_send(self):
        print("发送UDPTimeServer的数据")

class UDPEchoServer(UDPServer):
    def handle_receive(self):
        msg,addr = self.sock.recvfrom(8192)
        self.sock.sendto(msg,addr)

    def handle_send(self):
        print("发送UDPEchoServer的数据")


if __name__ == '__main__':
    handlers = [UDPEchoServer(('',14000)),UDPTimeServer(('',15000))]
    event_loop(handlers)