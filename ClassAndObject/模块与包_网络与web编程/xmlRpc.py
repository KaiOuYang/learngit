
from xmlrpc.server import SimpleXMLRPCServer

class KeyValueServer:
    #以下注册过的方法才能在 client中被使用，就是 client通过http post方法将 要调用的方法名称和相关参数传到
    #server端。 当客户端 s.set('foo','bar')即就代表着 要调用server端的已注册的set方法，并接收参数
    _rpc_methods_ =['get','set','delete','exists','keys']

    def __init__(self,address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address,allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self,name))


    def get(self,name):
        return self._data[name]

    def set(self,name,value):
        self._data[name]=value


    def delete(self,name):
        del self._data[name]

    def exists(self,name):
        return name in self._data

    def keys(self):
        return list(self._data)

    def serve_forever(self):
        self._serv.serve_forever()


if __name__ == '__main__':
    kvserv = KeyValueServer(('',15000))
    kvserv.serve_forever()