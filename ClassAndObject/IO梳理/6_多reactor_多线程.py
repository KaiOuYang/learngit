

import socket,select,threading,time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor,as_completed

results = []#列表的append与remove都是线程安全的

def superviseResult():#用于监控work结果是否到来
    print("superviseResult执行...")
    while True:#必然会占用分配给该线程的时间片走完，可否若都是阻塞则直接切换cpu呢
        time.sleep(2)
        print('results的元素个数为: ', len(results))
        #先将results中的元组拆出来
        futureResult = [itemFuture for itemFuture,rsend in results]
        for future in as_completed(futureResult):#若期物们都未完成，则会阻塞(是否会导致直接切换线程？)
            print('处理后results的元素个数为: ', len(futureResult))
            print("future结果为:")
            print(future.result())
            futureResult.remove(future)



class Worker():
    def __init__(self):
        pass

    @classmethod
    def work(self,data):
        print("current Thread is ",threading.current_thread().name)
        print("work()已接收到数据")
        return "success work!"


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
        resultFuture = self.pool.submit(Worker.work,data)#异步过程
        results.append((resultFuture,self.rObject))
        self.rObject.send(b'already submit to Worker')#此时拿不到result，所以需要另外处理


class Acceptor():
    def __init__(self,rItem):
        self.rObject = rItem

    def accepter(self):
        conn,addr = self.rObject.accept()
        return conn



class Dispatch():

    def __init__(self,sList,rList,server=None,pool=None):
        self.sList = sList
        self.rList = rList
        self.server = server
        self.pool = pool


    def dispatch(self):
        '''
        一个连接就得一个SubReactor线程
        :return:
        '''
        for rItem in self.rList:
            if rItem is self.server:#main使用时的dispatch逻辑
                acceptor = Acceptor(rItem)
                conn = acceptor.accepter()
                subThread = Thread(target=SubReactor.start,args=(conn,))#若只建一个sub线程，则需要主从线程 交互，用队列。此处可改为线程池
                subThread.start()
            else:#sub使用时的dispatch逻辑
                try:
                    handler = Handler(rItem,self.sList,self.pool)
                    handler.handle()#若在此处理resultFuture则必然会堵塞该SubReactor线程则后续的请求都会卡住，或专门拿一个线程出来监控等待结果返回?
                except ConnectionResetError as e:
                    self.sList.remove(rItem)
                    continue


class MainReactor():

    def start(self):
        server = socket.socket()
        address = ('127.0.0.1',8080)
        server.bind(address)
        print('listen...', address)
        server.listen(5)

        sList = []
        sList.append(server)
        resultSupervisor = Thread(target=superviseResult)
        resultSupervisor.daemon = True
        resultSupervisor.start()
        while True:#只管建立连接，建完连接后立马交给sub
            rList,wList,eList = select.select(sList,[],[])
            dispatchor = Dispatch(sList,rList,server=server)
            dispatchor.dispatch()

class SubReactor():

    @staticmethod
    def start(conn):
        print("current SubReactor Thread is ", threading.current_thread().name)
        sList = []
        sList.append(conn)
        pool = ThreadPoolExecutor(5)
        while True:
            rList,wList,eList = select.select(sList,[],[])
            dispatchor = Dispatch(sList,rList,pool=pool)
            dispatchor.dispatch()



if __name__ == '__main__':
    reactor = MainReactor()
    reactor.start()

