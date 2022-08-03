


class LoggedMappingMixin:

    __slots__ = ()

    def __getitem__(self, item):#就是代理模式，利用__mro__解析顺序性质，代理了一整个类
        print('Getting' + str(item))
        return super().__getitem__(item)


    def __setitem__(self, key, value):
        print("Settinig {} = {!r}".format(key,value))
        return super().__setitem__(key,value)


class LoggedDict(LoggedMappingMixin,dict):
    pass


if __name__ == '__main__':
    d = LoggedDict()
    print(LoggedDict.__mro__)
    d['x'] =1
    temp = d['x']