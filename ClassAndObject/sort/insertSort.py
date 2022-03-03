
from ClassAndObject.sort.common import countTime

@countTime
def insertSort(lists):
    '''目的将未排序区间的元素 插入到 已排序区间内， 所以外圈遍历未排序区间，即对于
    每个未排序元素，在已排序区间内找寻位置插入，一直保持有序区间有序即可（关键在于  已经有序的区间，若第一次比较不符合则后面都不用比较）'''
    length = len(lists)
    if length <= 1:
        return
    for i in range(1,length):#外圈表示 未排序区间，从1开始;
        value = lists[i]#保存 元素，使用该保存的元素进行比较，因有移动数据会将元素覆盖故先保存
        for j in range(i-1,-2,-1):#内圈表示 已排序区间（动态变化的故与外圈的i相关），倒序比较至0。若跳出循环表明已找到插入位置，并进行了数据移动，虚位以待
            if value < lists[j]:#每比较一次满足则向后移动一次(因必然已排序区间要让一个位置);  为找到插入位置
                lists[j+1] =lists[j]#移动数据，因后一个数据已经保存好
            else:
                break#若是break跳出，则表示需中间插入，又因多循环一次以致多减了1，故加j+1即为待插入位置
        lists[j+1] = value#插入待排序的数据，若不是break跳出内循环，则j可以循环到-1，表示插入到第1个位置；若
    # print(lists)



if __name__ == '__main__':
    import numpy as np
    listTest = np.random.randint(1000,size=10000)
    lists = [4,5,6,1,3,2]
    insertSort(lists)
    insertSort(listTest)
    # print(list(range(2,-1,-1)))