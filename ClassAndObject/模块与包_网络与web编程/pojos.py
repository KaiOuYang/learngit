
class Desc():

    def __init__(self,name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value



class StructureBase():#用于简化 实体类初始化

    _fileds=[]

    def __init__(self,*args,**kwargs):
        if len(args) > len(self._fileds):
            raise Exception("Expected %s arguments"%(len(self._fileds)))

        for key,value in zip(self._fileds,args):
            setattr(self,key,value)

        for name in self._fileds[len(args):]:
            setattr(self,name,kwargs.pop(name))

        if kwargs:
            raise TypeError("invalid arguments %s"%(','.join(kwargs)))




class Title(StructureBase):

    _fileds=["pic","desc","id"]

    pic = Desc("pic")
    desc = Desc("desc")
    id = Desc("id")

    def toDict(self):
        dictReturn = {}
        for name in self._fileds:
            value = getattr(self,name)
            dictReturn[name] = value
        return dictReturn

    def __repr__(self):
        strings = ','.join(['%s']*len(self._fileds))
        text = 'Title(%s)'%strings
        return text%tuple([self.__dict__[item] for item in self._fileds])

    def __str__(self):
        strings = ','.join(['%s']*len(self._fileds))
        text = '(%s)'%strings
        return text%tuple([self.__dict__[item] for item in self._fileds])


def typeassert(**kwargs):#未加入类型检测，若加则小修下Desc描述符
    def func(cls):
        for key,value in kwargs.items():
            setattr(cls,key,Desc(key))
        return cls
    return func


@typeassert(pic=str,desc=str,id=str)
class TitleMore(StructureBase):#相比于 Title类中自己手动一个个添加Desc描述符，用类装饰器+外参的方式 更简洁
    #因一旦 类属性的描述符数量过多，则会导致整个类看起来很臃肿
    _fileds=["pic","desc","id"]

    def toDict(self):
        dictReturn = {}
        for name in self._fileds:
            value = getattr(self,name)
            dictReturn[name] = value
        return dictReturn

    def __repr__(self):
        strings = ','.join(['%s']*len(self._fileds))
        text = 'Title(%s)'%strings
        return text%tuple([self.__dict__[item] for item in self._fileds])

    def __str__(self):
        strings = ','.join(['%s']*len(self._fileds))
        text = '(%s)'%strings
        return text%tuple([self.__dict__[item] for item in self._fileds])
if __name__ == '__main__':

    title = TitleMore(id = 4,desc = "3",pic = "8")
    print("title.__dict__ : ",title.__dict__)
    print(title.__class__.__dict__)
    print(title.toDict())
    print(title)
