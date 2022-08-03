


class BinarySearch:
    @staticmethod
    def binarySearchTarget(sourceList, target):
        left, right = 0, len(sourceList) - 1
        while (left <= right):
            mid = left + (right - left) // 2
            if sourceList[mid] == target:
                return mid
            elif sourceList[mid] < target:
                left = mid + 1
            elif sourceList[mid] > target:
                right = mid - 1
        return -1


    @staticmethod
    def binarySearchLeftBorder(sourceList,target):
        '''
        判定sourceList中<= target值的元素个数
        :param sourceList:
        :param target:
        :return:
        '''
        left,right = 0,len(sourceList)-1
        while(left <= right):
            mid = left + (right - left)//2
            if sourceList[mid] == target:
                right = mid -1#当left与right相等时，right又更新了一次，所以左边界情况应该最后返回left;
            elif sourceList[mid] < target:
                left = mid + 1
            elif sourceList[mid] > target:
                right = mid - 1
        if left >= len(sourceList):
            return -1
        return left


    @staticmethod
    def binarySearchRightBorder(sourceList,target):
        '''
        判定sourceList中<= target值的最后一个元素索引，再加1即为 小于等于target值的元素个数
        :param sourceList:
        :param target:
        :return:
        '''
        left,right = 0,len(sourceList)-1
        while(left <= right):#终止条件 left = right + 1，三种情况要么sourceList中有目标值的位置，要么全大于或全小于目标值
            mid = left + (right - left)//2
            if sourceList[mid] == target:
                left = mid + 1#当left与right相等时，left又更新了一次，所以右边界情况应该最后返回right
            elif sourceList[mid] < target:
                left = mid + 1
            elif sourceList[mid] > target:
                right = mid - 1
        if right < 0 :
            return -1
        return right


class ApplicationForBS:

    @staticmethod
    def sqrtRedo(target):
        if target > 1:
            low,high = 1,target
        else:
            low,high = target,1
        mid = 0
        while(abs(mid**2 - target) >= 0.000001):
            mid = low + (high - low)/2.0
            if mid**2 > target:
                high = mid
            elif mid**2 < target:
                low = mid
        return round(mid,6)

    @staticmethod
    def ip2num(ipString):
        one,two,three,four = ipString.split('.')
        num = int(four) + 256*int(three) + (256**2)*int(two) + (256**3)*int(one)
        return num

    @staticmethod
    def ipSearch(sources,target):
        ipDict = {ApplicationForBS.ip2num(item[0]):(item[2],ApplicationForBS.ip2num(item[1])) for item in sources}
        arraySource = sorted(ipDict.keys())
        numTarget = ApplicationForBS.ip2num(target)
        resultKey = BinarySearch.binarySearchRightBorder(arraySource,numTarget)
        numKey = arraySource[resultKey]
        value = ipDict[numKey]
        maxNumKey = value[1]
        if numTarget <= maxNumKey:
            ipString = value[0]
        else:
            ipString = '未知'
        return ipString

    @staticmethod
    def loopArrayBinarySearch(sourceArray,target):
        left,right = 0,len(sourceArray) - 1
        mid = left + (right - left)//2
        if sourceArray[mid]  == target:
            return  True
        elif sourceArray[mid] > sourceArray[0] and sourceArray[mid] > target:#尚未完成
            return BinarySearch.binarySearchTarget(sourceArray[left:mid+1],target)
        else:
            return ApplicationForBS.loopArrayBinarySearch(sourceArray[mid],target)




if __name__ == '__main__':
    # lists = [2,3,4,4,4,7,7,8,9]
    # target = 6
    # result = BinarySearch.binarySearchRightBorder(lists,target)
    # result2 = BinarySearch.binarySearchLeftBorder(lists,target)
    # print(result)
    # print(result2)

    import algrithom.commonConfig as common
    result = ApplicationForBS.ipSearch(common.ips,'202.102.48.256')
    print(result)