


def mergeSort(lists):
    length = len(lists)
    if length <= 1:
        return lists
    mergeSortIn(lists,0,length-1)#0到length-1，决定了传入的参数必须是都能取到的
    print(lists)

def mergeSortIn(A,p,r):
    if p >= r:
        return
    q = (p + r)//2
    mergeSortIn(A,p,q)
    mergeSortIn(A,q+1,r)
    merge(A,p,q,r)

def merge(A,p,q,r):
    tempList = []
    i,j = p,q+1
    while i<=q and j<=r:
        if A[i] < A[j]:
            tempList.append(A[i])
            i += 1
        else:
            tempList.append(A[j])
            j+= 1
    if i<q:#说明前一部分仍有数据
        tempList.extend(A[i:q+1])
    elif j<r:#说明后一部分仍有数据
        tempList += A[j:r+1]

    for ind in range(len(tempList)):#只覆盖排好序的那一部分
        A[p+ind] = tempList[ind]




if __name__ == '__main__':
    import numpy as np
    listTest = np.random.randint(500, size=500)
    lists = [ 1, 3, 2]
    mergeSort(lists)

