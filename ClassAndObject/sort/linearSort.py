import numpy as np


def calculateSort(A):
    '''
    计数排序 O(n)级别的时间复杂度
    :param A:
    :return:
    '''
    maxNum = max(A)
    saveList = [0]*len(A)
    countList = [0]*(maxNum+1)
    sumList = [0]*(maxNum+1)
    for item in A:
        countList[item] += 1
    for num in range(maxNum+1):
        tempList = countList[:num+1]
        sumList[num] = sum(tempList)
    for item in A[::-1]:#为保持稳定排序故反向进行
        indexTemp = sumList[item]
        saveList[indexTemp-1] = item
        sumList[item] -= 1
    return saveList




def baseNumSort(B):
    '''
    借用了框架 numpy，需要更进一步到底层即只用list，估计得用取余的方式
    :param B:
    :return:
    '''
    rows,cols = B.shape
    saveDict = {}
    for col in range(cols-1,-1,-1):
        sortBaseCol = B[:,col]
        for index,num in enumerate(sortBaseCol):
            saveDict.setdefault(num,[]).append(B[index].tolist())
        saveList = []
        for index in range(10):
            ele = saveDict.get(index,[])
            saveList.extend(ele)
        saveDict.clear()
        B = np.array(saveList)
    print(B)






