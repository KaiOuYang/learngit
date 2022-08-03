
from ClassAndObject.sort import selectSort,insertSort,maopao


if __name__ == '__main__':

    import numpy as np
    listTest = np.random.randint(100000,size=100000)
    # sortlistTest = sorted(listTest,reverse=True)

    insertSort.insertSort(listTest)

    selectSort.selectSort(listTest)
    # # selectSort.selectSort(sortlistTest)

    maopao.bubbleSortOptimize2(listTest)