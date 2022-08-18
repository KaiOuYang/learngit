

import socket,select





def reactor():
    server = socket.socket()
    address = ('127.0.0.1',8080)
    server.bind(address)
    print('listen...', address)
    server.listen(5)
    sList = []
    sList.append(server)
    while True:
        rList,wList,eList = select.select(sList,[],[])
        for rObject in rList:
            if rObject is server:
                conn,clientAddr = server.accept()
                sList.append(conn)
            else:
                try:
                    data = rObject.recv(1024)
                    if len(data) == 0:
                        sList.remove(rObject)
                        continue
                    rObject.send(b'bliblibli')
                except ConnectionResetError as e:
                    print("远端client主动断开连接")
                    sList.remove(rObject)
                    continue

class Acceptor():
    def __init__(self,sList,server):
        self.sList = sList
        self.server = server

    def startAccept(self):
        conn, clientAddr = self.server.accept()
        self.sList.append(conn)

class Handler():

    def __init__(self,rObject,sList):
        self.rObject = rObject
        self.sList = sList

    def startHandle(self):
        data = self.rObject.recv(1024)
        if len(data) == 0:
            self.sList.remove(self.rObject)
            return
        self.rObject.send(b'bliblibli')

class Dispatch():
    def __init__(self,rList,sList,server):
        self.rList = rList
        self.server = server
        self.sList = sList

    def dispatch(self):
        for rObject in self.rList:
            if rObject is self.server:
                acceptor = Acceptor(self.sList,self.server)
                acceptor.startAccept()
            else:
                try:
                    handler = Handler(rObject,self.sList)
                    handler.startHandle()
                except ConnectionResetError as e:
                    print("远端client主动断开连接")
                    self.sList.remove(rObject)
                    continue

class Reactor():
    server = socket.socket()
    address = ('127.0.0.1',8080)
    server.bind(address)
    print('listen...', address)
    server.listen(5)
    sList = []
    sList.append(server)

    while True:
        rList,wList,eList = select.select(sList,[],[])
        dispathor = Dispatch(rList,sList,server)
        dispathor.dispatch()




if __name__ == '__main__':
    reactor()



