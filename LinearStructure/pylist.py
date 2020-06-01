import numpy as np

class PyList(list):
    def __init__(self, content=[], size=20):
        super().__init__()
        self.items = [None] * size
        self.numItems = 0
        self.size = size
        for e in content:
            self.append(e)

    def __contains__(self, item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
        return False

    def __eq__(self, other):
        if (type(self) != type(other)):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if (self.items[i] != other.items[i]):
                return False
        return True

    def __setitem__(self, index, val):
        if index >= 0 and index <= self.numItems - 1:
            self.items[index] = val
            return
        print("the index is %d" % index)
        print("the limit is %d" % self.numItems)
        raise IndexError("Pylist assignment index out of range.")

    def __getitem__(self, index):
        if index >= 0 and index <= self.numItems - 1:
            return self.items[index]
        raise IndexError("Pylist index out of range.")

    def __iter__(self):
        for i in range(self.numItems):
            yield self.items[i]

    def append(self, item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1

    def __add__(self, other):
        result = PyList(size=self.numItems + other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result

    def insert(self, i, x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems - 1, i - 1, -1):
                self.items[j + 1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)

    def delete(self, index):
        if (self.numItems == self.size / 4):
            self.deallocate()
        if index >= self.numItems:
            raise IndexError("PyList index out of range.")
        else:
            for i in range(index, self.numItems - 1):
                self.items[i] = self.items[i + 1]
            self.numItems -= 1
            return

    def allocate(self):
        newlength = 2 * self.size
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength

    def deallocate(self):
        newlength = int(self.size / 2)
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength

    def delete_last(self, k):
        if k > self.numItems:
            self.numItems = 0
            self.size = 1
            self.items = [None] * self.size
            return
        else:
            rest = self.numItems - k
            self.numItems = rest
            while (self.numItems <= int(self.size / 4)):
                self.deallocate()
            return

    def swap(self, index1, index2):
        temp = self.items[index2]
        self[index2] = self[index1]
        self[index1] = temp

    def show(self):
        for i in range(self.numItems):
            print(self.items[i])

    # define selection sort
    def findMin(self):
        ans = 0
        for i in range(self.numItems):
            if self.items[i] < self.items[ans]:
                ans = i
        return ans

    def selectionSort(self):
        num = self.numItems
        result = []
        while num != 0:
            min_index = self.findMin()
            result.append(self.items[min_index])
            self.delete(min_index)
            num -= 1
        assert (self.numItems == 0)
        for i in result:
            self.append(i)
        return

    # define bubble sort
    def bubbleSort(self):
        # whole loop
        for i in range(self.numItems - 1):
            num_swap = 0
            # one pass
            for j in range(self.numItems - i - 1):
                if self.items[j] > self.items[j + 1]:
                    self.swap(j, j + 1)
                    num_swap += 1
            # one pass but nothing changes
            if num_swap == 0:
                return
        return

    # define merge sort
    def merge_add(self, left, mid, right):
        i = left
        j = mid + 1
        k = 0
        temp = PyList(self.items[left:right + 1], len(self.items[left:right + 1]))
        while i <= mid and j <= right:
            if self[i] < self[j]:
                temp[k] = self[i]
                i = i + 1
            else:
                temp[k] = self[j]
                j = j + 1
            k = k + 1
        while i <= mid:
            temp[k] = self[i]
            i = i + 1
            k = k + 1
        while j <= right:
            temp[k] = self[j]
            j = j + 1
            k = k + 1
        for i in range(temp.numItems):
            self[left + i] = temp[i]
        del temp

    def mergeSort(self, left=0, right=None):
        if right == None:
            right = self.numItems - 1
        if (left < right):
            mid = left + (right - left) // 2
            self.mergeSort(left, mid)
            self.mergeSort(mid + 1, right)
            self.merge_add(left, mid, right)

    # define the normal insertion sort
    def original_insertionSort(self):
        for i in range(1, self.numItems):
            key = self[i]
            j = i-1
            while j >=0 and self[j]>key:
                # the key is too small that it has to be put forward
                self[j+1] = self[j]
                j-=1
            self[j+1] = key

    # define the improved insertion sort
    def binarySearch(self, value, start, end):
        mid = (start + end) // 2
        if self[mid] == value:
            assert (type(start) == int)
            return mid
        if start == end:
            # then value is a little smaller than self[start]
            assert (type(start) == int)
            return start
        elif self[mid] < value:
            # go to right half
            return self.binarySearch(value, mid + 1, end)
        elif self[mid] > value:
            # go to the left half
            return self.binarySearch(value, start, mid)

    def move_elements(self, value, index, cur_index):
        for i in range(cur_index, index, -1):
            self[i] = self[i - 1]
        self[index] = value

    def insertionSort(self):
        for i in range(1, self.numItems):
            # this will loop from the start to the beginning
            value = self[i]
            if value >= self[i - 1]:
                continue
            else:
                index = self.binarySearch(value, 0, i - 1)
                self.move_elements(value, index, i)

    # def mergeSortTHR(self):
    def mergeSortTHR(self, left=0, right=None, thr=10):
        if right == None:
            right = self.numItems - 1
        # add one threshold
        if (right - left + 1) < thr:
            self.mergeSortBubble(left, right)
        else:
            mid = left + (right - left) // 2
            self.mergeSortTHR(left, mid, thr)
            self.mergeSortTHR(mid + 1, right, thr)
            self.merge_add(left, mid, right)

    def mergeSortBubble(self, left, right):
        # whole loop
        numItems = right - left + 1
        for i in range(numItems - 1):
            num_swap = 0
            # one pass
            for j in range(left, left + numItems - i - 1):
                if self.items[j] > self.items[j + 1]:
                    self.swap(j, j + 1)
                    num_swap += 1
            # one pass but nothing changes
            if num_swap == 0:
                return
        return

    # define the quick sort
    def qsort(self):
        self.__qsort(0, self.numItems-1)

    def __qsort(self, left, right):
        if left>=right:
            return
        pivot = self[right]
        i = j = left
        while self[i] < pivot:
            i+=1
            j+=1
        while j < right:
            if self[j] < pivot:
                self.swap(i, j)
                i+=1
            j+=1
        self.swap(i, right)
        self.__qsort(left, i-1)
        self.__qsort(i+1, right)

    # define the radix sort
    def radixsort(self, k=10):
        round = 0
        flag = 1
        while flag:
            flag = 0
            bucket = [[] for i in range(k)]
            for i in self:
                # print(type(i))
                q = i // (k ** round)
                if q != 0:
                    flag = 1
                bucket[q % k].append(i)
            self.items = []
            for i in bucket:
                self.items = self.items + i
            round += 1

class SPyList(PyList):
    def __init__(self, contents=[], size=10):
        self.items = [None] * size
        self.keys = []  # all the "key" values of input dictionary
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)

    def append(self, item):
        if (type(item) is not dict):
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if (item['key'] in self.keys):  # modification
            raise KeyError("Key already exists")
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1
        self.keys.append(item['key'])  # modification

    def __setitem__(self, index, val):
        # example:
        # original list is: [{'key': 1, 'B': 'bbbb', 'D': 'yyyy'}, {xxxxxx}, None, None, ...]
        # input thing: {'key': 1, 'B': 'b', 'Y': 'y'}
        # after spylist[0] = {'key': 1, 'B': 'b', 'Y': 'y'}
        # the result will be [{'key': 1, 'B': 'b', 'D': 'y'}, {xxxxxx}, None, None, ...]
        if (type(val) is not dict):
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if 0 <= index < self.numItems:
            old_key = self.items[index]['key']  # modification
            if (val['key'] != old_key and val['key'] in self.keys):
                raise KeyError("Key already exists")
            self.keys.remove(old_key)
            self.keys.append(val['key'])
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")

    def __add__(self, other):
        raise SyntaxError("Add operation not defined")  # modification

    def insert(self, i, x):
        if (type(x) is not dict):
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if (x['key'] in self.keys):  # modification
            raise KeyError("Key already exists")
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems - 1, i - 1, -1):
                self.items[j + 1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
            self.keys.append(x['key'])
        else:
            self.append(x)

    def projection(self, projectList):
        # ask for values of some keys like "A", "B"
        newContent = []
        for item in self.items:
            if (item == None):
                continue
            newItem = {}
            for key in item.keys():
                if (key in projectList):
                    newItem[key] = item[key]
            newContent.append(newItem)
        return PyList(newContent)

    def projection_without_duplicate(self, projectList):
        newContent = []
        for item in self.items:
            if (item == None):
                continue
            newItem = {}
            for key in item.keys():
                if (key in projectList):
                    newItem[key] = item[key]
            newContent.append(newItem)
        # If there are duplicated elements, raise an error
        for i in range(len(newContent) - 1):
            if (newContent[i] in newContent[i + 1:]):
                raise ValueError("Duplicated records after projection")
        return PyList(newContent)

    def sort_by_key(self):
        # implement the merge sort method
        self.__mergeSort(0, self.numItems-1)

    def get_key(self, index):
        item = self[index]
        if item is None:
            raise KeyError("None object doesn't have key")
        return item["key"]

    def __mergeSort(self, left, right):
        if left >= right:
            return
        mid = left + (right - left)//2
        self.__mergeSort(left, mid)
        self.__mergeSort(mid+1, right)
        self.__merge_add(left, mid, right)

    def __merge_add(self, left, mid, right):
        i = left
        j = mid+1
        temp = []
        while i<=mid and j<=right:
            if self.get_key(i) < self.get_key(j):
                temp.append(self[i])
                i+=1
            else:
                temp.append(self[j])
                j+=1
        while i<=mid:
            temp.append(self[i])
            i+=1
        while j<=right:
            temp.append(self[j])
            j+=1
        assert(len(temp) == right - left + 1)
        for item in temp:
            self.items[left] = item
            left+=1
        del temp

if __name__ == "__main__":
    content1 = list(np.random.randint(0,1000, size=20))
    content2 = list(np.random.randint(0, 1000, size=20))
    content3 = list(np.random.randint(0, 1000, size=20))
    content4 = list(np.random.randint(0, 1000, size=20))
    pylist1 = PyList(content1, size = 100)
    pylist1.qsort()
    pylist1.show()
    print("--------")
    pylist2 = PyList(content2)
    pylist2.mergeSort()
    pylist2.show()
    print("--------")
    pylist3 = PyList(content3)
    pylist3.original_insertionSort()
    pylist3.show()
    print("--------")
    pylist4 = PyList(content4)
    pylist4.radixsort()
    pylist4.show()
    # s1 = SPyList([{'key': 3, 'A': 'a', 'X': 'x', 'Y': 'y'}, {'key': 1, 'B': 'b', 'Y': 'y'}, {'key': 2, 'C': 'c', 'Z': 'z'}])
    # print(s1.items)
    # print(s1.keys)
    # projectionlist = ["A", "B", "C"]
    # s1.projection(projectionlist).show()
    # s1.sort_by_key()
    # print(s1.items)

