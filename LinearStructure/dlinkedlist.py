#  DN<=>A<=>B<=>C<=>D<=> ...<=>Z<=>(back to Dummy Node)
# ↑
# first
class DLinkedList:
    class __Node:
        def __init__(self, item=None, next=None, previous=None):
            self.item = item
            self.next = next
            self.previous = previous

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

    def __init__(self, contents=[]):
        self.first = DLinkedList.__Node(None, None, None)
        self.numItems = 0
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        for e in contents:
            self.append(e)

    def printList(self):
        tmp = self.first.next
        nodes = []
        for i in range(self.numItems):
            nodes.append(str(tmp.item))
            tmp = tmp.next
        print(' <-> '.join(nodes))

    def append(self, item):
        lastNode = self.first.getPrevious()
        newNode = DLinkedList.__Node(item, self.first, lastNode)
        lastNode.setNext(newNode)
        self.first.setPrevious(newNode)
        self.numItems += 1

    def locate(self, index):
        if 0 <= index < self.numItems:
            cursor = self.first.getNext()
            for _ in range(index):
                cursor = cursor.getNext()
            return cursor
        raise IndexError("DLinkedList index out of range")

    # define the splice method
    def splice(self, index, other, index1, index2):
        if index1 <= index2:
            begin = other.locate(index1)
            end = other.locate(index2)
            self.insertList(begin, end, index)
            self.numItems += index2 - index1 + 1

    def insertList(self, begin, end, index):
        address = self.locate(index)
        successor = address.getNext()
        begin.setPrevious(address)
        end.setNext(successor)
        address.setNext(begin)
        successor.setPrevious(end)

    # the selection sort
    def SelectionSort(self):
        firstNode = self.first.getNext()
        lastNode = self.first.getPrevious()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        counter = self.numItems
        outlast = self.first
        while counter != 0:
            location = self.getMinimum(firstNode, lastNode)
            if location == firstNode:
                firstNode = location.getNext()
            else:
                if location == lastNode:
                    lastNode = location.getPrevious()
                else:
                    self.cut(firstNode, lastNode, location)
            self.addLocation(outlast, location)
            outlast = location
            counter -= 1

    # selection sort helper: getMinimum() determines the node with the minimum item
    def getMinimum(self, first, last):
        minimum = first.getItem()
        cursor = first
        location = first
        while cursor != last:
            cursor = cursor.getNext()
            item = cursor.getItem()
            if item < minimum:
                minimum = item
                location = cursor
        return location

    # selection sort helper: cut() deletes the node with the minimum item from the inlist:
    def cut(self, first, last, location):  # location is actually the min node that you found
        prev = location.getPrevious()
        next = location.getNext()
        prev.setNext(next)
        next.setPrevious(prev)

    # selection sort helper: addLocation()adds the node with the minimum item to the outlist
    def addLocation(self, outlast, location):
        location.setPrevious(outlast)
        location.setNext(self.first)
        outlast.setNext(location)
        self.first.setPrevious(location)

    # the insertion sort
    def InsertionSort(self):
        cursor = self.first.getNext()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        while cursor != self.first:
            cursor1 = cursor.getNext()  # keep a record of the next cursor position
            self.addout(cursor)
            cursor = cursor1

    def addout(self, cursor):
        cursor2 = self.first.getNext()
        while (cursor2 != self.first and cursor2.getItem() < cursor.getItem() and cursor2.getNext() != self.first):
            cursor2 = cursor2.getNext()
        if cursor2 != self.first and cursor2.getItem() >= cursor.getItem():  # insert before cursor2
            previous = cursor2.getPrevious()
            previous.setNext(cursor)
            cursor.setNext(cursor2)
            cursor.setPrevious(previous)
            cursor2.setPrevious(cursor)
        else:  # insert at the end of the output
            cursor2.setNext(cursor)
            cursor.setNext(self.first)
            cursor.setPrevious(cursor2)
            self.first.setPrevious(cursor)

    # the bubble sort
    def swap(self, obj1, obj2):
        prev_obj1 = obj1.getPrevious()
        next_obj2 = obj2.getNext()
        prev_obj1.setNext(obj2)
        obj2.setPrevious(prev_obj1)
        obj1.setNext(next_obj2)
        next_obj2.setPrevious(obj1)
        obj2.setNext(obj1)
        obj1.setPrevious(obj2)

    def BubbleSort(self):
        # firstNode corresponds to index 0
        firstNode = self.first.getNext();
        # secondNode corresponds to index 1
        secondNode = firstNode.getNext()
        if firstNode == self.first or secondNode == self.first:
            return
        for i in range(self.numItems - 1):
            num_swap = 0
            for j in range(self.numItems - i - 1):
                if firstNode.getItem() > secondNode.getItem():
                    self.swap(firstNode, secondNode)
                    num_swap += 1
                    # increment the objects after being swapped
                    secondNode = firstNode.getNext()
                else:
                    # increment to objects as index increases
                    firstNode = firstNode.getNext()
                    secondNode = secondNode.getNext()
            if num_swap == 0:
                return
            firstNode = self.first.getNext();
            secondNode = firstNode.getNext()
        return

    # merge sort
    def helper_split(self):
        index = self.numItems//2
        cursor = self.locate(index)
        lastNode1 = cursor.getPrevious()
        lastNode2 = self.first.getPrevious()
        self.first.setPrevious(lastNode1)
        lastNode1.setNext(self.first)
        secondList = DLinkedList([])
        secondList.first.setNext(cursor)
        cursor.setPrevious(secondList.first)
        lastNode2.setNext(secondList.first)
        secondList.first.setPrevious(lastNode2)
        temp = self.numItems
        self.numItems = index
        secondList.numItems = temp - index
        return secondList

    def MergeSort(self):
        if self.numItems <= 4:
            self.BubbleSort()
        else:
            secondList = self.helper_split()
            self.MergeSort()
            secondList.MergeSort()
            self.merge(secondList)
            del secondList
        return

    def merge(self, secondList):
        total_length = self.numItems + secondList.numItems
        firstNode = self.first.getNext()
        secondNode = secondList.first.getNext()
        dummyNode = self.__Node()
        head = dummyNode
        while firstNode != self.first and secondNode != secondList.first:
            if firstNode.getItem() < secondNode.getItem():
                dummyNode.setNext(firstNode)
                firstNode.setPrevious(dummyNode)
                firstNode = firstNode.getNext()
            else:
                dummyNode.setNext(secondNode)
                secondNode.setPrevious(dummyNode)
                secondNode = secondNode.getNext()
            dummyNode = dummyNode.getNext()
        if firstNode == self.first:
            dummyNode.setNext(secondNode)
            secondNode.setPrevious(dummyNode)
            while secondNode != secondList.first:
                secondNode = secondNode.getNext()
            secondNode.getPrevious().setNext(self.first)
            self.first.setPrevious(secondNode.getPrevious())
        elif secondNode == secondList.first:
            dummyNode.setNext(firstNode)
            firstNode.setPrevious(dummyNode)
        self.first.setNext(head.getNext())
        head.getNext().setPrevious(self.first)
        del head
        self.numItems = total_length

    # print out the list
    def show(self):
        temp = self.first.getNext()
        while temp != self.first:
            print(temp.getItem())
            temp = temp.getNext()


c = DLinkedList(list(range(30,0,-1)))
c.printList()
print("after the sort")
c.BubbleSort()
c.printList()
