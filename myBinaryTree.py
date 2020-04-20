class BST:
    class __Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def __iter__(self):
            if self.left != None:
                for elem in self.left:
                    yield elem
            yield self.val
            if self.right != None:
                for elem in self.right:
                    yield elem

    def __init__(self):
        self.root = None

    def __iter__(self):
        if self.root != None:
            return self.root.__iter__()
        else:
            return [].__iter__()

    def insert(self, val):
        self.__insert(self, self.root, None, val)

    @staticmethod
    def __insert(tree, root, parent, val, direction=0):
        if root is None:
            if direction == 1:
                node = BST.__Node(val)
                parent.right = node
            elif direction == 0:
                node = BST.__Node(val)
                tree.root = node
            else:
                node = BST.__Node(val)
                parent.left = node
            return
        if root.val > val:
            BST.__insert(tree, root.left, root, val, -1)
        elif root.val < val:
            BST.__insert(tree, root.right, root, val, 1)
        else:
            # same value inserted
            return

    def find(self, val):
        def __find(root, val):
            if root == None:
                return False
            if val == root.val:
                return True
            if val < root.val:
                return __find(root.left, val)
            else:
                return __find(root.left, val)

        return __find(self.root, val)

    def delete(self, val):
        self.__delete(self, self.root, None, val)

    @staticmethod
    def __delete(tree, node, parent, val, direction=0):
        def helper(parent, node, direction):
            if direction == 1:
                parent.right = node
            elif direction == -1:
                parent.left = node
            else:
                tree.root = node
        if node is None:
            return
        if val < node.val:
            BST.__delete(tree, node.left, node, val,  -1)
        elif val > node.val:
            BST.__delete(tree, node.right, node, val, 1)
        elif val == node.val:
            # the core part of the delete
            if node.right is None and node.left is None:
                # leaf's deletion
                helper(parent, None, direction)
            elif node.right is not None and node.left is not None:
                # two child deletion
                temp = node.left
                while temp.right is not None:
                    temp = temp.right
                node.item = temp.item
                BST.__delete(tree, node.left, node, node.item, -1)
            else:
                # one child's deletion
                if node.left is None:
                    node = node.right
                    helper(parent, node, direction)
                else:
                    node = node.left
                    helper(parent, node, direction)


if __name__ == "__main__":
    import numpy as np
    bst = BST()
    content = np.random.randint(0,100,size=15)
    for i in content:
        bst.insert(i)
    for i in bst:
        print(i)
