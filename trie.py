class Trie:
    class TrieNode:
        def __init__(self,item,next=None,follows=None):
            self.item = item
            self.next = next
            self.follows = follows

    def __init__(self):
        self.start = None

    def insert(self,item):
        if type(item) is not list:
            item = list(item)
        self.start = Trie.__insert(self.start,item)

    def __contains__(self,item):
        if type(item) is not list:
            item = list(item)
        return Trie.__contains(self.start,item+["#"])

    @staticmethod
    def __insert(node,item):
        if item == []:
            newnode = Trie.TrieNode("#")
            return newnode
        if node == None:
            key = item.pop(0)
            newnode = Trie.TrieNode(key)
            newnode.follows = Trie.__insert(newnode.follows,item)
            return newnode
        else:
            key = item[0]
            if node.item == key:
                key = item.pop(0)
                node.follows = Trie.__insert(node.follows,item)
            else:
                node.next = Trie.__insert(node.next,item)
            return node

    @staticmethod
    def __contains(node,item):
        if item == []:
            return True
        if node == None:
            return False
        key = item[0]
        if node.item == key:
            key = item.pop(0)
            return Trie.__contains(node.follows,item)
        return Trie.__contains(node.next,item)

    # a print function which can print out structure of tries
    # to help better understand
    def show(self):
        self.print_trie(self.start)

    def print_trie(self, root, level_f=0):
        if(root == None):
            return
        if(root.item != '#'):
            print(root.item, '-', end='')
        else:
            print(root.item, end='')
        self.print_trie(root.follows, level_f+1)
        if(root.next!=None):
            print('\n')
            str_sp = ' '*level_f*3
            print(str_sp+'|')
            print(str_sp, end='')
        self.print_trie(root.next,level_f)
        return

# modified class -- only store unique prefix
class Trie_m:
    class TrieNode:
        def __init__(self, item, next=None, follows=None):
            self.item = item
            self.next = next
            self.pre = None
            self.follows = follows

    def __init__(self):
        self.start = None
        self.key_endnode_dict = {}
        self.prefix_dict = {}

    def insert(self, item):
        keys = ''.join(item)
        self.start = Trie_m.__insert(self, self.start, item, keys)
        #         for key in self.key_endnode_dict.keys():
        #             node = self.key_endnode_dict[key]
        #             suffix = ''
        #             if(node.next != None):
        #                 suffix = ''
        #             else:
        #                 while(node.pre != None and node.pre.next == None):
        #                     suffix += node.item
        #                     node = node.pre
        #                 suffix = list(suffix[:-1])
        #                 suffix.reverse()
        #             prefix = list(keys)[:(len(item_c) - len(suffix))]
        #             self.prefix_dict[keys] = prefix
        self.findPrefix()

    def findPrefix(self):
        for key in self.key_endnode_dict.keys():
            node = self.key_endnode_dict[key]
            suffix = ''
            if (node.next != None):
                suffix = ''
            else:
                while (node.pre != None and node.next == None):
                    suffix += node.item
                    node = node.pre
                suffix = list(suffix[:-1])
                suffix.reverse()
            prefix = list(key)[:(len(key) - len(suffix))]
            self.prefix_dict[key] = prefix

    #         self.key_endnode_dict[item] = # last node
    def __insert(self, node, item, keys):
        if item == []:
            newnode = Trie_m.TrieNode("#")
            self.key_endnode_dict[keys] = newnode
            return newnode
        if node == None:
            key = item.pop(0)
            #             print(key)
            newnode = Trie_m.TrieNode(key)
            newnode.follows = Trie_m.__insert(self, newnode.follows, item, keys)
            newnode.follows.pre = newnode
            return newnode
        else:
            key = item[0]
            #             print(key)
            if node.item == key:
                key = item.pop(0)
                node.follows = Trie_m.__insert(self, node.follows, item, keys)
                node.follows.pre = node
            else:
                node.next = Trie_m.__insert(self, node.next, item, keys)
            #                 node.next.pre = node
            return node

    # a print function which can print out structure of tries
    # to help better understand
    def print_trie(self, root, level_f):
        if (root == None):
            return
        if (root.item != '#'):
            print(root.item, '-', end='')
        else:
            print(root.item, end='')
        self.print_trie(root.follows, level_f + 1)
        if (root.next != None):
            print('\n')
            str_sp = ' ' * level_f * 3
            print(str_sp + '|')
            print(str_sp, end='')
        self.print_trie(root.next, level_f)
        return

    def __contains__(self, item):
        if (''.join(item) in self.prefix_dict.keys()):
            return True
        return False


trie = Trie()
trie.insert("apple")
trie.insert("google")
trie.insert("huawei")
trie.insert("xiaomi")
trie.insert("arm")
trie.show()