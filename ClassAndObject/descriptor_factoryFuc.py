import abc


class FruitDescriptor:

    # __count = 0

    def __init__(self,arg):
        self.arg = arg
        # cls = self.__class__
        # prefix = cls.__name__
        # self.arg = "%s#%s"%(prefix,cls.__count)
        # cls.__count += 1

    def __get__(self, instance, owner):
        print("descriptor __get__")
        if instance is None:
            return self
        return instance.__dict__[self.arg]


    # def __set__(self, instance, value):
    #     print("descriptor __set__")
    #     if value > 0:
    #         instance.__dict__[self.arg] = value
    #     else:
    #         raise ValueError("should be > 0")

    def __delete__(self, instance):
        pass



class DescriptorAutoStorage:

    __count = 0

    def __init__(self):
        cls = self.__class__
        name = cls.__name__
        self.storage = "{}#{}".format(name,cls.__count)

    # def __get__(self, instance, owner):
    #     if instance is None:
    #         return self
    #     return getattr(instance,self.storage)

    def __set__(self, instance, value):
        setattr(instance,self.storage,value)


class Validated(abc.ABC,DescriptorAutoStorage):

    def __set__(self, instance, value):
        value = self.validated(value)
        super().__set__(instance,value)

    @abc.abstractmethod
    def validated(self,val):
        pass


class AppelFruitDescriptor(Validated):
    def validated(self,val):
        if val <0:
            raise ValueError("should be > 0")
        return val

class PearFruitDescriptor(Validated):
    def validated(self,val):
        if len(val) == 0:
            raise  ValueError("val can not be empty")
        return val



class Customer:

    apple = AppelFruitDescriptor()
    pear = PearFruitDescriptor()

    # banana = FruitDescriptor("banana")

    def __init__(self):
        self.apple = 1
        self.pear = "2"
        # self.banana = 3
        # self.func =5

    def __repr__(self):
        return "Customer({0.apple},{0.pear})".format(self)

    def __str__(self):
        return "({0.apple},{0.pear})".format(self)

    def func(self):
        pass


def func1():
    pass

if __name__ == '__main__':
    customer = Customer()
    # customer.apple = 3
    # customer.banana =4
    # Customer.banana =2
    # print(Customer.banana)
    print(Customer.func)
    print(customer.func)

    # print(Customer.__dict__)
    # print(customer.pear)
    # print(customer.__dict__)
