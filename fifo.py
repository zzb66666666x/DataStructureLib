class Fifo:
    def __init__(self,size=20):
        self.items = [None] * size
        self.first = 0
        self.last = -1
        self.size = size
        self.length = 0
    def computelength(self):
        if self.last > self.first:
            self.length = self.last - self.first + 1
        else:
            self.length = self.last - self.first + 1 + self.size
    def isEmpty(self):
        if self.length != 0:
            return False
        return True
    def front(self):
        if self.length != 0:
            return self.items[self.last]
        raise Exception("Queue is empty")
    def back(self):
        if self.length != 0:
            return self.items[self.first]
        raise Exception("Queue is empty")
    def pushback(self,item):
        if self.length == self.size:
            self.allocate()
        self.last = (self.last + 1) % self.size
        self.items[self.last] = item
        self.computelength()
    def popfront(self):
        if self.length == self.size / 4:
            self.deallocate()
        if self.last - self.first + 1 != 0:
            frontelement = self.items[self.first]
            self.first = (self.first + 1) % self.size
            self.computelength()
            return frontelement
        raise Exception("Queue is empty")
    def allocate(self):
        newlength = 2 * self.size
        newQueue = [None] * newlength
        for i in range(self.size):
            #core part#
            #use (i+first) mod size to get our elements
            pos = (i + self.first) % self.size
            ###########
            newQueue[i] = self.items[pos]
        self.items = newQueue
        self.first = 0
        self.last = self.size - 1
        self.size = newlength
        self.computelength()
    def deallocate(self):
        newlength = self.size / 2
        newQueue = [None] * newlength
        length = (self.last - self.first +1) % self.size
        for i in range(length):
            pos = (i + self.first) % self.size
            newQueue[i] = self.items[pos]
        self.items = newQueue
        self.first = 0
        self.last = length - 1
        self.size = newlength
        self.computelength()
    def __iter__(self):
        rlast = self.first + self.length
        for i in range(self.first,rlast):
            yield self.items[i % self.size]

class Queue:
    class __Node:
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self, content=[]):
        self.head = None
        self.end = None
        for i in content:
            self.enqueue(i)

    def enqueue(self, val):
        node = self.__Node(val)
        if self.end is None:
            assert (self.head is None)
            self.head = self.end = node
        else:
            self.end.next = node
            self.end = node

    def dequeue(self):
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head is None:
            self.end = None
        return node.val

    def is_empty(self):
        if self.head is None:
            assert (self.end is None)
            return True
        return False

    def show(self):
        temp = self.head
        while temp is not None:
            print(temp.val)
            temp = temp.next


queue = Fifo()
for i in range(20):
    queue.pushback(i)
print(queue.items)
print(queue.first)
print(queue.last)
for i in range(5):
    a = queue.popfront()
    print("pop out:", a)
print(queue.items)
print(queue.first)
print(queue.last)
for i in range(20,23):
    queue.pushback(i)
print(queue.items)
print(queue.first)
print(queue.last)
for i in range(24,30):
    queue.pushback(i)
print(queue.items)
print(queue.first)
print(queue.last)
# for x in queue:
#     print(x)
# print(queue.size,queue.length)