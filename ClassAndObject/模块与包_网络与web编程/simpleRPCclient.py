


import pickle,json

class RPCProxy:#分工明确，值得学习，proxy包含 client即代理该client，围绕该client进行发送接收前置的逻辑(即动态代理的功能增加)
    def __init__(self,connection):
        self._connection =connection

    def __getattr__(self, name):#作为装饰器传递外参的方式
        def do_rpc(*args,**kwargs):
            self._connection.send(json.dumps((name,args,kwargs)))
            result = json.loads(self._connection.recv())
            if isinstance(result,Exception):
                raise result
            return result
        return do_rpc

if __name__ == '__main__':
    from multiprocessing.connection import Client
    c = Client(('localhost',17000),authkey=b'peekaboo')
    proxy = RPCProxy(c)
    proxy.add(2,3)