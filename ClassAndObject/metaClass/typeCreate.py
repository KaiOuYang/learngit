

def fn(self,name="come here"):
    print(name)

class HelloOringe():

    def hehe(self,name="come here"):
        print(name)

Hello = type('Hello',(object,),dict(hehe = fn))

if __name__ == '__main__':
    hello = Hello()
    print(hello.hehe())