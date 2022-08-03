

class Desc:

    def __init__(self,name = None,**opts):
        self.name = name
        for key,val in opts.items():
            setattr(self,key,val)

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Type(Desc):
    expected_type = type(None)

    def __set__(self, instance, value):
        print("走到了 Type")
        if not isinstance(value,self.expected_type):
            raise TypeError("should be %s"%self.expected_type)
        super().__set__(instance,value)#得用 super().__set__方法，使得在mro上链式调用，否则无法在各个维度进行验证校验


class Unsigned(Desc):

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("should be >= 0")
        super().__set__(instance,value)


class MaxSize(Desc):
    def __init__(self,name,**opt):
        if 'size' not in opt:
            raise TypeError("missing size option")
        super().__init__(name,**opt)

    def __set__(self, instance, value):
        print("走到了 MaxSize")
        if len(value) >= self.size:
            raise ValueError("size must be <")
        super().__set__(instance,value)




class Integer(Type):
    expected_type = int


class String(Type):
    expected_type = str

class SizedString(String,MaxSize):
    '''继承 String,MaxSize，故首先进行Type中的__set__校验，当通过后会调用super().__set__从而
    在 SizedString类的mro上寻找下一个 __set__即找到了 MaxSize中，使用其中的__set__进行校验，完成
    后继续调用super().__set__即最后调用到 Desc中的__set__做最后的赋值与设置。  __init__方法原理同样'''
    pass


class Stock:
    name = SizedString('name',size=8)


    def __init__(self,name):
        self.name = name

if __name__ == '__main__':
    s = Stock('yk')
    # s.name = 'k45134616k'
    print(s)