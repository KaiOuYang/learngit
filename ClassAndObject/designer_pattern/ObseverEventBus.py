from abc import ABC, abstractmethod

from threading import Thread
from concurrent.futures import ThreadPoolExecutor


class UserBusinuessController():
    def __init__(self, userService):
        self.userService = userService


    def register(self, name, password):
        userId = self.userService.register(name, password)
        return userId


class UserProxyController(UserBusinuessController):
    '''
    业务代理模式类 隔离业务与非业务即解耦不同功能
    '''

    def __init__(self):
        super().__init__()
        self.eventBus = EventBus()
        # self.eventBus = AsyncEventBus()

    def setRegObservers(self,observers):
        for ob in observers:
            self.eventBus.register(ob)

    def register(self, name, password):
        userId = super().register(name, password)
        self.eventBus.post(userId)
        return userId

class EventBus():


    def register(self,ob):
        pass

    def post(self,idname):
        pass


def subsribeDecorator(func):
    def subsribe_eventbus(*args,**kwargs):
        result = func(*args,**kwargs)
        return result
    return subsribe_eventbus


class Listener(ABC):
    '''
    观察者抽象类，即解耦不同行为
    '''

    @abstractmethod
    def runAction(self, name):
        pass


class MsgListener(Listener):
    '''
    信息发送方式
    '''

    @subsribeDecorator
    def runAction(self, name):
        print("msg to %s" % name)


class PhoneListener(Listener):
    '''
    电话发送方式
    '''

    @subsribeDecorator
    def runAction(self, name):
        print("phone to %s" % name)


