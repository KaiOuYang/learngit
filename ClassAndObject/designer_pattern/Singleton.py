

import threading

class Singleton():
    _instance_lock = threading.Lock()


    def __new__(cls, *args, **kwargs):#饿汉式
        '''实例化对象时，先执行了类的__new__方法，然后再执行类的__init方法'''
        if not hasattr(cls,'instance'):
            with cls._instance_lock:
                if not hasattr(cls,'instance'):#加锁为防止 多线程 创建出多例
                    cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        import time
        time.sleep(1)
        pass


    # @classmethod
    # def get_instance(cls,*args,**kwargs):
    #
    #     return

def task(arg):
    obj = Singleton()
    print(obj)


if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=task,args=[i,])
        t.start()