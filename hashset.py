class HashSet:
    def __init__(self, contents=[]):
        self.items = [None] * 20
        self.numItems = 0
        for e in contents:
            self.add(e)

    def __len__(self):
        return self.numItems

    def add(self, item):
        if HashSet.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self.items, [None] * 2 * len(self.items))

    def __contains__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] != None:
            if self.items[index] == item:
                return True
            index = (index + 1) % len(self.items)
        return False

    def delete(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 20) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None] * (len(self.items) // 2))
        else:
            raise KeyError("Item not in HashSet")

    def __iter__(self):
        for item in self.items:
            if item is not None and type(item) is not HashSet.__Placeholder:
                yield item

    # ===== Hidden Class =====
    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

    # ===== Auxiliary Functions =====
    # They all have '__' as prefixes to indicate that they are private methods to the class
    @staticmethod
    def __add(item, items):
        index = hash(item) % len(items)
        location = -1
        while items[index] != None:
            if items[index] == item:
                return False
            if location < 0 and type(items[index]) == HashSet.__Placeholder:
                location = index
            index = (index + 1) % len(items)
        if location < 0:
            location = index
        items[location] = item
        return True

    @staticmethod
    def __rehash(olditems, newitems):
        for e in olditems:
            if e != None and type(e) != HashSet.__Placeholder:
                HashSet.__add(e, newitems)
        return newitems

    @staticmethod
    def __remove(item, items):
        index = hash(item) % len(items)
        while items[index] != None:
            if items[index] == item:
                nextIndex = (index + 1) % len(items)
                if items[nextIndex] == None:
                    items[index] = None
                else:
                    items[index] = HashSet.__Placeholder()
                return True
            index = (index + 1) % len(items)
        return False

    def __getitem__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if self.items[index] == item:
                return self.items[index]
            index = (index + 1) % len(items)
        raise KeyError("No such item stored")

    def __setitem__(self, olditem, newitem):
        index = hash(olditem) % len(self.items)
        while self.items[index] is not None:
            if self.items[index] == olditem:
                self.items[index] = newitem
                return
            index = (index + 1) % len(self.items)

class HashMap:
    class __KVPair:
        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __eq__(self, other):
            if type(self) != type(other):
                return False
            return self.key == other.key

        def getKey(self):
            return self.key

        def getValue(self):
            return self.value

        def __hash__(self):
            # 重构了hash函数，使得复用HashSet的add成为可能
            return hash(self.key)

    def __init__(self, content):
        content = self.__convert(content)
        self.hSet = HashSet(content)

    def __convert(self, content):
        ans = []
        for i in content:
            ans.append(HashMap.__KVPair(i[0], i[1]))
        return ans

    def __len__(self):
        return len(self.hSet)

    def __contains__(self, item):
        return HashMap.__KVPair(item, None) in self.hSet

    def not__contains__(self, item):
        return item not in self.hSet

    def __setitem__(self, key, value):
        test = HashMap.__KVPair(key, None)
        if test in self.hSet:
            # modify the value
            self.hSet[test] = HashMap.__KVPair(key, value)
        else:
            self.hSet.add(HashMap.__KVPair(key, value))

    def __getitem__(self, key):
        item = HashMap.__KVPair(key, None)
        if item in self.hSet:
            val = self.hSet[item].getValue()
            return val
        raise KeyError("Key " + str(key) + " not in HashMap")

    def __iter__(self):
        for x in self.hSet:
            yield x.getKey(),x.getValue()


hmap = HashMap([(1,"A"),(2,"B"),(3,"C"),(4,"D"),(5,"E")])
print(hmap[5])
for i in hmap:
    print(i)
hmap[5] = "F"
print(hmap[5])

