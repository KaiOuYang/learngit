

import socket,select,threading
from concurrent.futures import ThreadPoolExecutor


class Worker():
    def __init__(self):
        pass

    @classmethod
    def work(self,data):
        print("current Thread is ",threading.current_thread().name)
        print("work()已接收到数据")


class Handler():
    def __init__(self,rItem,sList,pool):
        self.rObject = rItem
        self.sList = sList
        self.pool = pool

    def handle(self):
        '''
        处理的是请求而不是连接，一个连接可有多个请求，所以线程池资源会很快用尽，因一个线程就得处理一个请求。
        因pool.submit是异步过程，所以线程执行完的result此时拿不到，需要收集起来处理
        :return:
        '''
        data = self.rObject.recv(1024)
        if len(data) == 0:
            self.sList.remove(self.rObject)
            return
        result = self.pool.submit(Worker.work,data)#异步过程
        self.rObject.send(b'already submit to Worker')#此时拿不到result，所以需要另外处理


class Acceptor():
    def __init__(self,rItem,sList):
        self.rObject = rItem
        self.sList = sList

    def accepter(self):
        conn,addr = self.rObject.accept()
        self.sList.append(conn)



class Dispatch():

    def __init__(self,sList,rList,server,pool):
        self.sList = sList
        self.rList = rList
        self.server = server
        self.pool = pool

    def dispatch(self):
        for rItem in self.rList:
            if rItem is self.server:
                acceptor = Acceptor(rItem,self.sList)
                acceptor.accepter()
            else:
                try:
                    handler = Handler(rItem,self.sList,self.pool)
                    handler.handle()
                except ConnectionResetError as e:
                    self.sList.remove(rItem)
                    continue


class Reactor():

    def start(self):
        server = socket.socket()
        address = ('127.0.0.1',8080)
        server.bind(address)
        print('listen...', address)
        server.listen(5)

        sList = []
        sList.append(server)
        pool = ThreadPoolExecutor(5)
        while True:
            rList,wList,eList = select.select(sList,[],[])
            dispatchor = Dispatch(sList,rList,server,pool)
            dispatchor.dispatch()



if __name__ == '__main__':
    reactor = Reactor()
    reactor.start()
