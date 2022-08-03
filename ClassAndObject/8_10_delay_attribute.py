import math

class delayDesc:
    def __init__(self,func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            val = self.func(instance)
            setattr(instance,self.func.__name__,val)
            return val


class Circle:

    def __init__(self,radius):
        self.radius = radius

    @delayDesc#本质上是链式调用
    def area(self):#将绑定方法 作为参数传递到 类delayDesc的__init__中，形成的 delayDesc实例再赋值到 area上， 即 area = delayDesc(area)
        return math.pi * self.radius**2

if __name__ == '__main__':

    c = Circle(3)
    print(c.area)
    print(c)