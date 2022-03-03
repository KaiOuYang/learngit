from ClassAndObject.sort.common import countTime

@countTime
def selectSort(lists):
    length = len(lists)
    if length <= 1:
        return

    for i in range(length):#外圈循环开始表示找寻有序区该序号的元素，循环完成1次表示已确定一个有序区的元素
        minValue = lists[i]
        for j in range(i,length):#内圈表示每次从无序区比较出最小元素
            if lists[j] < minValue:
                lists[j], minValue = minValue, lists[j]#经交换后,minValue标签到新的一个对象
                lists[i] = minValue#故需要再赋值给 lists[i]
    # print(lists)

if __name__ == '__main__':
    import numpy as np
    listTest = np.random.randint(500,size=500)
    print(listTest)
    lists = [4, 5, 6, 1, 3, 2]
    selectSort(listTest)