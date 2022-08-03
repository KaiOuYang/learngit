import math


class CatheProperty:

    def __init__(self,func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value

def CatheProperty1(func):
    def funcInner(*args):
        result = func(*args)
        return result
    return funcInner

class Circle:
    '''
    缓存的实现，本质是非覆盖型描述符与实例变量的优先级差异体现。所以首先将该方法转化为 描述符类，那就得用装饰器类
    进行装饰，使得该方法转化为一个类，且该类实现__get__方法即变为描述符类。在该__get__方法中计算出相应的值后设置
    到对应的托管类的实例变量，此时缓存已完成。
    若是以方法的方式，即用装饰器函数进行装饰，则达不到缓存的效果，因不易于给托管类设置对应的实例属性值。
    '''
    def __init__(self,radius):
        self.radius = radius

    @CatheProperty
    def area(self):
        return 3.14 * self.radius ** 2


if __name__ == '__main__':

    circle = Circle(3)
    a = circle.area
    print(a())
    print(circle.__dict__)
    print(circle.__class__.__dict__)