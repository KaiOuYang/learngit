

import pickle,json
class RPCHandler:#分工明确，值得学习 server包含 listener、handler、多线程或池化逻辑。
    #handler名称的职责是 处理完成连接并从内核copy数据到用户态的数据即recv
    # （先监听即listen，后建立连接,并继续监听，再数据是否就绪是由accept来确定，数据内核态搬运至用户态由recv或read执行）
    #所以 必然监听与建立连接是另外模块（一个服务器）做的，传入即可，也是一种解耦
    def __init__(self):
        self._functions={}

    def register_function(self,func):
        self._functions[func.__name__] = func


    def handle_connection(self,connection):
        try:
            while True:
                func_name,args,kwargs = json.loads(connection.recv())#无线循环等待数据就绪
                try:
                    r = self._functions[func_name](*args,**kwargs)
                    connection.send(json.dumps(r))
                except Exception as e:
                    connection.send(json.dumps(e))
        except EOFError:
            pass


from multiprocessing.connection import Listener
from threading import Thread

def rpc_server(handler,address,authkey):
    sock = Listener(address,authkey=authkey)#返回已经建立连接的sock
    while True:
        client = sock.accept()#检查数据是否就绪(即是否从网卡缓冲区运到内核缓冲区)，若未就绪将会堵塞在此?
        t = Thread(target=handler.handle_connection,args=(client,))
        t.daemon =True
        t.start()


def add(x,y):
    print(x+y)
    return x+y

def sub(x,y):
    print(x-y)
    return x-y

if __name__ == '__main__':

    handler = RPCHandler()
    handler.register_function(add)
    handler.register_function(sub)
    print("listen port:17000 ...")
    rpc_server(handler,('localhost',17000),authkey=b'peekaboo')