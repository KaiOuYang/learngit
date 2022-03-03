


def childGen():
    total = 0
    count = 0
    average = 0
    while True:
        item = yield
        if item is None:
            break
        total += item
        count += 1
        average = total/count
    return count,average

def proxyGen(result,key):
    while True:
        result[key] = yield from childGen()

def foo():
    item = yield
    if item is None:
        return 2

def bigFoo():
    while True:
        print(1)
        a = foo()
        next(a)
        a.send(None)



if __name__ == '__main__':

    # newDict = {
    #     'hill':[1,2,3,4,5,6],
    #     'peggy':[7,8,9,10,11,12],
    #     'bobby':[13,14,15,16,17,18]
    # }
    #
    # result = {}
    # for key,values in newDict.items():
    #     pipeGen = proxyGen(result,key)
    #     next(pipeGen)
    #     for item in values:
    #         pipeGen.send(item)
    #     try:
    #         pipeGen.send(None)
    #     except StopIteration as e:
    #         print(e.value)
    # print(result)

    bigFoo()



