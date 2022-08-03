
class Person:

    def __init__(self,name):
        self._name = name

    @property
    def name(self):
        print("get _name")
        return self._name


    @name.setter
    def name(self,value):
        print("set _name")
        if not isinstance(value,str):
            raise TypeError("Expected a string")
        self._name = value


class SubPerson(Person):

    @property
    def name(self):
        print('Getting name')
        # temp = super()
        # print("get %s"%temp)
        return super().name#此处为实例变量

    @name.setter
    def name(self,value):
        print("Setting name %s"%value)
        # temp = super(SubPerson,SubPerson)
        # print("set %s"%temp)
        super(SubPerson,SubPerson).name.__set__(self,value)#此处为类变量


if __name__ == '__main__':

    s = SubPerson("Guido")
    print(s.name)
    s.name = "yk"
    print(s.name)