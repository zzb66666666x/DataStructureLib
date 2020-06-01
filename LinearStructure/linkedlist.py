#  DN<=>A=>B=>C=>D=> ...=>Z
# ↑                     ↑
# first                 last
class LinkedList:
    class __Node:
        def __init__(self, item, next=None):
            self.item = item
            self.next = next

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

    def __init__(self, contents=[]):
        self.first = LinkedList.__Node(None, None)  # ,None)
        self.numItems = 0
        self.first.setNext(self.first)
        self.last = self.first
        for e in contents:
            self.append(e)

    def printList(self):
        tmp = self.first.next
        nodes = []
        for i in range(self.numItems):
            nodes.append(str(tmp.item))
            tmp = tmp.next
        print(' -> '.join(nodes))

    def getPrevious(self, cursor, node):
        tmp = cursor
        while (tmp.next != node):
            tmp = tmp.next
        return tmp

    def append(self, item):
        lastNode = self.last
        newNode = LinkedList.__Node(item, self.first)  # ,lastNode)
        lastNode.setNext(newNode)
        self.last = newNode
        self.numItems += 1

    def locate(self, index):
        if index >= 0 and index < self.numItems:
            cursor = self.first.getNext()
            for _ in range(index):
                cursor = cursor.getNext()
            return cursor
        raise IndexError("LinkedList index out of range")

    def splice(self, index, other, index1, index2):
        if index1 <= index2:
            begin = other.locate(index1)
            end = other.locate(index2)
            self.insertList(begin, end, index)
            self.numItems += index2 - index1 + 1

    def insertList(self, begin, end, index):
        address = self.locate(index)
        successor = address.getNext()
        end.setNext(successor)
        address.setNext(begin)

    def SelectionSort(self):
        firstNode = self.first.getNext()
        lastNode = self.last
        self.first.setNext(self.first)
        counter = self.numItems
        outlast = self.first
        while counter != 0:
            location = self.getMinimum(firstNode, lastNode)
            if location == firstNode:
                firstNode = location.getNext()
            else:
                if location == lastNode:
                    lastNode = self.getPrevious(firstNode, location)
                else:
                    self.cut(firstNode, lastNode, location)
            self.addLocation(outlast, location)
            outlast = location
            self.last = location  # update last pointer
            counter -= 1
        self.last.next = None

    # dgetMinimum() determines the node with the minimum item
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

    # cut() deletes the node with the minimum item from the inlist:
    def cut(self, first, last, location):  # location is actually the min node that you found
        prev = self.getPrevious(first, location)
        next = location.getNext()
        prev.setNext(next)

    # addLocation()adds the node with the minimum item to the outlist
    def addLocation(self, outlast, location):
        location.setNext(self.first)
        outlast.setNext(location)

    def InsertionSort(self):
        cursor = self.first.getNext()
        self.first.setNext(self.first)
        while cursor != self.first:
            cursor1 = cursor.getNext()  # keep a record of the next cursor position
            self.addout(cursor)
            cursor = cursor1
        tmp = self.first.next
        for i in range(self.numItems - 1):  # sanity check settings
            tmp = tmp.next
        self.last = tmp
        self.last.next = None

    def addout(self, cursor):
        cursor2 = self.first.getNext()
        while (cursor2 != self.first and cursor2.getItem() < cursor.getItem() and cursor2.getNext() != self.first):
            cursor2 = cursor2.getNext()
        if cursor2 != self.first and cursor2.getItem() >= cursor.getItem():  # insert before cursor2
            previous = self.getPrevious(cursor, cursor2)
            previous.setNext(cursor)
            cursor.setNext(cursor2)
        else:  # insert at the end of the output
            cursor2.setNext(cursor)
            cursor.setNext(self.first)