
from socket import socket,AF_INET,SOCK_STREAM

import select
import os
import sys
from multiprocessing import Queue


class SingletonReactor:
    def __init__(self,address):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.bind(address)
        self.socket.setblocking(False)
        self.socket.listen(1)
        self.message_queues = {}

    def startService(self):
        print("Single reactor mode start")
        inputs = []
        outputs = []
        inputs.append(self.socket)
        while True:
            readable,sendable,exceptional = select.select(inputs,outputs,[])
            for item in readable:
                if item is self.socket:#建立连接
                    connection,client_address = item.accept()#从全连接队列中拿出之前新建的已连接socket
                    print("连接来自于: ",client_address)
                    inputs.append(connection)
                    self.message_queues[connection] = Queue()
                else:
                    data = item.recv(1024)
                    if data != '':
                        self.message_queues[item].put(data)
                        if item not in outputs:
                            outputs.append(item)
                    else:
                        if item in outputs:
                            outputs.remove(item)
                        inputs.remove(item)
                        item.close()


class Acceptor:
    def __init__(self,socket):
        pass

class Handler:
    pass

if __name__ == '__main__':
    s = SingletonReactor(('',8000))
    s.startService()