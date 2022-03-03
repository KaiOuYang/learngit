
class Decriptor:

    def __init__(self,name=None,**opts):
        self.name = name
        for key,value in opts.items():
            setattr(self,key,value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value



def Typed(expected_type,cls=None):
    if cls is None:
        return lambda cls:Typed(expected_type,cls)
    super_set = cls.__set__#得新打个标签，否则会导致无限循环

    def __set__(self,instance,value):
        if not isinstance(value,expected_type):
            raise TypeError('expected' + str(expected_type))
        super_set(self,instance,value)

    cls.__set__ = __set__
    return cls


def Unsigned(cls):
    super_set = cls.__set__

    def __set__(self,instance,value):
        if value <0:
            raise ValueError("Expected >= 0")
        super_set(self,instance,value)
    cls.__set__ = super_set
    return cls

def MaxSized(cls):#加货后替换

    super_init = cls.__init__

    def __init__(self,name=None,**opts):
        if 'size' not in opts:
            raise TypeError("missing size option")
        super_init(self,name,**opts)

    cls.__init__ = super_init

    super_set = cls.__set__

    def __set__(self,instance,value):
        if len(value) > self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self,instance,value)

    cls.__set__ = __set__

    return cls


@Typed(int)#装饰器先运行外层，返回一个匿名函数再将 integer类作为参数传入
class Integer(Decriptor):
    pass

@Unsigned
class UnsignedInteger(Integer):
    pass

if __name__ == '__main__':
    integer = Integer()
    print(intt)