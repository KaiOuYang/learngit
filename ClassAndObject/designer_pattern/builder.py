










class Person():

    def __init__(self,bulider):
        self.name = bulider.name
        self.age = bulider.age
        self.height = bulider.height
        self.weight = bulider.weight

    class Builder():

        def __init__(self):
            self.name = '无'
            self.age = 18
            self.height = 175
            self.weight = 120

        def setName(self,name):
            if name == '':
                raise ValueError("name 不能为空")
            self.name = name
            return self

        def setAge(self,age):
            if age < 18:
                raise ValueError("age 必须大于18")
            self.age = age
            return self

        def setHeight(self,height):
            if height < 170:
                raise ValueError("height 必须大于 170")
            self.height = height
            return self

        def setWeight(self,weight):
            if weight >200:
                raise ValueError("weight 必须小于 200")
            self.weight = weight
            return self

        def build(self):#都有之后统一注入到外部类中
            '''年龄大于25 且体重小于170 则 身高必须大于180'''
            if self.age>25 and self.weight <170:
                if self.height < 180:
                    raise ValueError("身高不符合条件")
            return Person(self)

if __name__ == '__main__':

    if __name__ == '__main__':
        specifiedPerson = Person.Builder().setName('rxk').setAge(27).setHeight(180).setWeight(150).build()
        print(specifiedPerson.name)
        print(specifiedPerson.age)
        print(specifiedPerson.height)
        print(specifiedPerson.weight)
        print(dir(specifiedPerson))
