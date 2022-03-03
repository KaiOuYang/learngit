
class funcPropertyDescriptor:

    def __init__(self,storage_name):
        self.storage_name = storage_name

    def __get__(self,instance,owner):
        print(owner)
        return instance.__dict__[self.storage_name]

    def __set__(self,instance,val):
        if val > 0:
            instance.__dict__[self.storage_name] = val
        else:
            raise ValueError("should be > 0")

    def __delete__(self, instance):
        pass


def funcProperty(arg:str):#arg参数得自己保存，即闭包保存，get(propertyObj)时只传入实例self

    def arg_getter(instance):
        return instance.__dict__[arg]

    def arg_setter(instance,val):
        if val > 0:
            instance.__dict__[arg] = val
        else:
            raise ValueError("should be > 0")

    return property(arg_getter,arg_setter)


class Pair:

    h = funcPropertyDescriptor("_h")
    z = funcProperty("_z")

    def __init__(self):
        self._x = 1
        self._y = 2
        self._z = 3
        self._h = 4

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


    def __repr__(self):
        return "Pair({0._x},{0._y})".format(self)

    def __str__(self):
        return "({0._x!s},{0._y!s})".format(self)


if __name__ == '__main__':
    pair = Pair()
    a = pair.h
    print(pair.__class__)