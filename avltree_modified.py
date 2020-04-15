# this the major program for AVLTree structure
import numpy as np

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


class AVLTree:
    class AVLNode:
        def __init__(self, item, balance=0, left=None, right=None):
            self.item = item
            self.balance = balance
            self.left = left
            self.right = right
            self.parent = None

        def __iter__(self):
            if self.left is not None:
                for elem in self.left:
                    yield elem
            yield self.item, self.balance
            if self.right is not None:
                for elem in self.right:
                    yield elem

        def show(self):
            print("\n######")
            print("item: ", self.item)
            print("balance: ", self.balance)
            if self.left != None:
                print("left: ", self.left.item)
            if self.right != None:
                print("right: ", self.right.item)
            print("#####")

    def __init__(self):
        self.root = None

    def __iter__(self):
        if self.root is not None:
            return self.root.__iter__()
        else:
            return [].__iter__()

    @staticmethod
    def iterDFS(root):
        # using the pre-order: root--left--right
        if root is not None:
            yield root.item
        else:
            return
        if root.left is not None:
            for i in AVLTree.iterDFS(root.left):
                yield i
        if root.right is not None:
            for j in AVLTree.iterDFS(root.right):
                yield j

    @staticmethod
    def iterBFS(root):
        queue = Queue()
        assert (root is not None)
        queue.enqueue(root)
        while not queue.is_empty():
            node = queue.dequeue()
            yield node.item
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)

    def rangeDFS(self, x, y):
        iterator = self.iterDFS(self.root)
        for i in iterator:
            if i >= x and i < y:
                yield i

    def rangeBFS(self, x, y):
        iterator = self.iterBFS(self.root)
        for i in iterator:
            if i >= x and i < y:
                yield i

    def insert(self, item):
        def __insert(root, item):
            newtree = AVLTree.AVLNode(item)
            stack = []
            badChild = None
            while root is not None:
                if item < root.item:
                    stack.insert(0, (root, -1))
                    if root.left is None:
                        root.left = newtree
                        return stack, badChild
                    if root.balance == -1:
                        badChild = root.left
                    root = root.left
                else:
                    stack.insert(0, (root, 1))
                    if root.right is None:
                        root.right = newtree
                        return stack, badChild
                    if root.balance == 1:
                        badChild = root.right
                    root = root.right

        if self.root is None:
            self.root = AVLTree.AVLNode(item)
            stack = []
            badChild = None
        else:
            result = __insert(self.root, item)
            stack = result[0]
            badChild = result[1]
        rotTree = None
        badGrandchild = None
        for N in stack:
            node = N[0]
            inc = N[1]
            if rotTree is not None:
                if inc == 1:
                    node.right = rotTree
                else:
                    node.left = rotTree
                return
            newbal = node.balance + inc
            if badChild == node:
                if inc == 1:
                    badGrandchild = node.right
                else:
                    badGrandchild = node.left
            if newbal == 0:
                node.balance = 0
                return
            if -1 <= newbal <= 1:
                node.balance = newbal
            else:
                if inc == 1:
                    if badChild.right == badGrandchild:
                        # now the badGrandchild is at the right of badChild
                        rotTree = AVLTree.__rotateLeft(node, badChild, 0, 0)
                    else:
                        # now the badGrandchild is not at the right of badChild: first right rotate then left
                        # variable item represents the inserted value
                        if item < badGrandchild.item:
                            # in this case, the final balance for badChild will be 1
                            n, c = 0, 1
                        else:
                            if item > badGrandchild.item:
                                # in this case, the final balance for the problem root node will have balance -1
                                # because it will be shifted left
                                n, c = -1, 0
                            else:
                                n, c = 0, 0
                        rotTree1 = AVLTree.__rotateRight(badChild, badGrandchild, c, 0)
                        rotTree = AVLTree.__rotateLeft(node, rotTree1, n, 0)
                else:
                    if badChild.left == badGrandchild:
                        rotTree = AVLTree.__rotateRight(node, badChild, 0, 0)
                    else:
                        if item < badGrandchild.item:
                            n, c = 0, -1
                        else:
                            if item > badGrandchild.item:
                                n, c = 1, 0
                            else:
                                n, c = 0, 0
                        rotTree1 = AVLTree.__rotateLeft(badChild, badGrandchild, c, 0)
                        rotTree = AVLTree.__rotateRight(node, rotTree1, n, 0)
        if rotTree is not None:
            self.root = rotTree

    @staticmethod
    def __rotateLeft(node, child, nbal, cbal):
        node.right = child.left
        node.balance = nbal
        child.left = node
        child.balance = cbal
        return child

    @staticmethod
    def __rotateRight(node, child, nbal, cbal):
        node.left = child.right
        node.balance = nbal
        child.right = node
        child.balance = cbal
        return child

    def find(self, item):
        def __find(root, item):
            if root is None:
                return False
            if item == root.item:
                return True
            if item < root.item:
                return __find(root.left, item)
            else:
                return __find(root.right, item)

        return __find(self.root, item)

    def delete(self, item):
        def __findandreturn(root, item):
            if root == None:
                return [], root, False
            if item == root.item:
                return [(root, 0)], root, True
            if item < root.item:
                result = __findandreturn(root.left, item)
                stack1 = result[0]
                stack1.append((root, 1))
                return stack1, result[1], result[2]
            else:
                result = __findandreturn(root.right, item)
                stack1 = result[0]
                stack1.append((root, -1))
                return stack1, result[1], result[2]

        def __findswapLeft(node, prev):
            stack = []
            while node.left is not None:
                stack.insert(0, (node, 1))
                prev = node
                node = node.left
            minitem = node.item
            if stack == []:
                prev.right = node.right
            else:
                prev.left = node.right
            return (minitem, stack)

        def __findswapRight(node, prev):
            stack = []
            while node.right is not None:
                stack.insert(0, (node, -1))
                prev = node
                node = node.right
            maxitem = node.item
            if stack == []:
                prev.left = node.right
            else:
                prev.right = node.left
            return maxitem, stack

        result = __findandreturn(self.root, item)
        if result[2] is False:
            return
        stack1 = result[0]
        start = stack1.pop(0)
        startnode = start[0]
        startinc = start[1]
        nextRight = startnode.right
        nextLeft = startnode.left
        stack = []
        if startnode.balance == 1:
            result = __findswapLeft(nextRight, startnode)
            stack = result[1]
            startnode.item = result[0]
            startinc = -1
        else:
            if startnode.balance == -1:
                result = __findswapRight(nextLeft, startnode)
                stack = result[1]
                startnode.item = result[0]
                startinc = 1
            else:
                if startnode.right != None:
                    if nextRight.balance != 1:
                        result = __findswapLeft(nextRight, startnode)
                        stack = result[1]
                        startnode.item = result[0]
                        startinc = -1
                    else:
                        result = __findswapRight(nextLeft, startnode)
                        stack = result[1]
                        startnode.item = result[0]
                        startinc = 1
                else:
                    if self.root == startnode:
                        self.root = None
                        return
                    last = stack1.pop(0)
                    lastnode = last[0]
                    if last[1] == 1:
                        lastnode.left = None
                    else:
                        lastnode.right = None
                    stack1.insert(0, (lastnode, last[1]))
                    startnode = None
        if startnode != None:
            start = (startnode, startinc)
            stack1.insert(0, start)
        stack = stack + stack1
        stack2 = iter(stack + [(None, 0)])
        next(stack2)
        for N in stack:
            currentnode = N[0]
            increment = N[1]
            NN = next(stack2)
            rotTree = None
            stop = False
            newbal = currentnode.balance + increment
            if -1 <= newbal <= 1:
                currentnode.balance = newbal
                if newbal != 0:
                    stop = True
            else:
                if increment == 1:
                    badChild = currentnode.right
                    badGrandchild = badChild.left
                    if badChild.balance == 0:
                        rotTree = AVLTree.__rotateLeft(currentnode, badChild, 1, -1)
                        stop = True
                    else:
                        if badChild.balance == 1:
                            rotTree = AVLTree.__rotateLeft(currentnode, badChild, 0, 0)
                        else:
                            nbal, cbal = 0, 0
                            if badGrandchild.balance == 1:
                                nbal = -1
                            if badGrandchild.balance == -1:
                                cbal = 1
                            rotTree1 = AVLTree.__rotateRight(badChild, badGrandchild, cbal, 0)
                            rotTree = AVLTree.__rotateLeft(currentnode, rotTree1, nbal, 0)
                else:
                    badChild = currentnode.left
                    badGrandchild = badChild.right
                    if badChild.balance == 0:
                        rotTree = AVLTree.__rotateRight(currentnode, badChild, -1, 1)
                        stop = True
                    else:
                        if badChild.balance == -1:
                            rotTree = AVLTree.__rotateRight(currentnode, badChild, 0, 0)
                        else:
                            nbal, cbal = 0, 0
                            if badGrandchild.balance == 1:
                                cbal = -1
                            if badGrandchild.balance == -1:
                                nbal = 1
                            rotTree1 = AVLTree.__rotateLeft(badChild, badGrandchild, cbal, 0)
                            rotTree = AVLTree.__rotateRight(currentnode, rotTree1, nbal, 0)
            if rotTree is not None:
                if NN[0] is not None:
                    if NN[1] == 1:
                        NN[0].left = rotTree
                    if NN[1] == -1:
                        NN[0].right = rotTree
                else:
                    self.root = rotTree
            if stop is True:
                return

    def node_number(self, root=None):
        if root is None:
            return AVLTree.__node_number(self.root)
        else:
            return AVLTree.__node_number(root)

    @staticmethod
    def __node_number(root):
        if(root is None):
            return 0
        left = AVLTree.__node_number(root.left)
        right = AVLTree.__node_number(root.right)
        return left+right+1

    def clear_all(self):
        def __clear(root):
            if root is None:
                return
            left = root.left
            right = root.right
            root.left = None
            root.right = None
            __clear(left)
            __clear(right)

        __clear(self.root)
        self.root = None

    def median_insert(self, item):
        # this function guarantee the median property of avl tree
        iterator = self.iterDFS(self.root)
        temp = [item]
        for i in iterator:
            if i is not None:
                temp.append(i)
        self.clear_all()
        quick_sort(temp, 0, len(temp) - 1)
        self.clear_all()
        median_list = median_number_order(temp)
        for i in median_list:
            self.insert(i)

    def median_delete(self, item):
        temp = []
        for i in self:
            temp.append(i[0])  # 把原AVL树的元素全部加到temp列表，且这个列表一定是有序的
        temp.remove(item)  # 去掉要删除的元素
        median_list = median_number_order(temp)
        self.clear_all()
        for i in median_list:
            self.insert(i)

def median_number_order(ele):
    res_list = []
    temp_list = [ele]
    while True:
        for i in temp_list:
            res_list.append(i[(len(i) - 1) // 2])  # 把每个list以中间数分成两个list，中间数加到res_list
            if len(i) >= 1:
                if i[((len(i) - 1) // 2 + 1):] != []:
                    temp_list.insert(temp_list.index(i), i[((len(i) - 1) // 2 + 1):])
                if i[:(len(i) - 1) // 2] != []:
                    temp_list.insert(temp_list.index(i), i[:(len(i) - 1) // 2])
                temp_list.remove(i)
            elif len(i) == 0:
                temp_list.remove(i)
            if temp_list == []:
                return res_list

def swap(array, a, b):
    temp = array[a]
    array[a] = array[b]
    array[b] = temp

def quick_sort(content, left, right):
    if left >= right:
        return
    pivot_index = np.random.randint(left, right + 1)
    pivot = content[pivot_index]
    swap(content, pivot_index, right)
    i = j = left
    while content[i] < pivot:
        i += 1
        j += 1
    while j < right:
        if content[j] < pivot:
            swap(content, i, j)
            i += 1
        j += 1
    swap(content, i, right)
    quick_sort(content, left, i - 1)
    quick_sort(content, i + 1, right)


if __name__ == "__main__":
    avl = AVLTree()
    content = [12, 7, 19, 21, 14, 13]

    # testing insert
    print("testing insert")
    for value in content:
        avl.insert(value)
    for i in avl:
        print(i)

    # testing delete
    print("testing delete")
    avl.delete(19)
    avl.delete(21)
    avl.delete(7)
    avl.delete(13)
    avl.delete(14)
    for i in avl:
        print(i)
    avl.insert(19)
    avl.insert(21)
    avl.insert(13)
    avl.insert(14)
    avl.insert(7)

    print("test node number")
    print(avl.node_number()) # answer should be 6

    # # testing the DFS and BFS
    # print("tests of search method")
    # it1 = avl.iterDFS(avl.root)
    # for i in it1:
    #     print(i)
    # print("BFS then")
    # it2 = avl.iterBFS(avl.root)
    # for j in it2:
    #     print(j)
    # print("testing rangeBFS")
    # for value in avl.rangeBFS(10, 15):
    #     print(value)
    # print("testing rangeDFS")
    # for value2 in avl.rangeDFS(10, 20):
    #     print(value2)

    # # testing median insert
    # print("test of median properties")
    # print("###the test of insert###")
    # mtree = AVLTree()
    # content = [6, 4, 8, 7, 2, 10, 5, 9, 1, 12]
    # for i in content:
    #     mtree.median_insert(i)
    # for i in mtree:
    #     print(i)
    # mtree.root.show()
    # mtree.root.left.show()
    # mtree.root.right.show()
    # mtree.root.left.left.show()
    # mtree.root.left.right.show()
    # mtree.root.right.left.show()
    # mtree.root.right.right.show()
    # # tests of the median delete
    # print("\n###the test of delete###")
    # mtree.clear_all()
    # mtree.insert(8)
    # mtree.insert(5)
    # mtree.insert(9)
    # mtree.insert(2)
    # mtree.insert(6)
    # mtree.insert(10)
    # mtree.median_delete(10)
    # for i in mtree:
    #     print(i)
    # mtree.root.show()
    # mtree.root.left.show()
    # mtree.root.right.show()
    # mtree.root.left.right.show()
    # mtree.root.right.right.show()
