from abc import ABC,abstractmethod

from threading import Thread
from concurrent.futures import ThreadPoolExecutor

class UserBusinuessController():
    def __init__(self,list_listen,userService):
        self.listens = list(list_listen)
        self.userService = userService

    def setListen(self,listenOb):
        self.listens.append(listenOb)

    def register(self,name,password):
        userId = self.userService.register(name,password)
        return userId

class UserProxyController(UserBusinuessController):
    '''
    业务代理模式类 隔离业务与非业务即解耦不同功能
    '''
    def register(self,name,password):
        userId = super().register(name,password)
        for listen in self.listens:
            with ThreadPoolExecutor(max_workers=5) as t:
                t.submit(listen.runAction,userId)

        return userId


class Listener(ABC):
    '''
    观察者抽象类，即解耦不同行为
    '''
    @abstractmethod
    def runAction(self,name):
        pass


class MsgListener(Listener):
    '''
    信息发送方式
    '''
    def runAction(self,name):
        print("msg to %s"%name)


class PhoneListener(Listener):
    '''
    电话发送方式
    '''
    def runAction(self,name):
        print("phone to %s"%name)