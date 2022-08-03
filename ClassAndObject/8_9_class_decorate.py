

class Typed:
    def __init__(self,name,expected_type):
        self.name = name
        self.expected_type =expected_type

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]


    def __set__(self, instance, value):
        if not isinstance(value,self.expected_type):
            raise TypeError("Expected" + str(self.expected_type))
        instance.__dict__[self.name] = value

def typeassert(**kwargs):
    def decorate(cls):
        for name,expected_type in kwargs.items():
            setattr(cls,name,Typed(name,expected_type))
        return cls
    return decorate


@typeassert(name=str,shares=int,price=float)#用类装饰器的方式 为指定类添加遵循描述符协议的类属性
class Stock:# 本质上是链式调用   Stock = typeassert(name=str,shares=int,price=float)(Stock)
    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price


if __name__ == '__main__':
    s = Stock('yk',1,2.0)
    print(s.__class__.__dict__)