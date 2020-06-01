# this is the Robin Hood Hashing for E4

class HashSet:
    class __Item:
        def __init__(self, val):
            self.val = val
            self.collision = 0

    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

    def __init__(self, contents=[]):
        self.items = [None] * 20
        self.numItems = 0
        for e in contents:
            self.add(e)

    def __iter__(self):
        for item in self.items:
            if item is not None and type(item) != HashSet.__Placeholder:
                yield item.val

    def add(self, item):
        if HashSet.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self.items, [None] * 2 * len(self.items))

    @staticmethod
    def __add(item, items):
        index = hash(item) % len(items)
        item_obj = HashSet.__Item(item)
        location = -1
        while items[index] is not None:
            if location < 0 and type(items[index]) == HashSet.__Placeholder:
                # check if we find a free block
                location = index
                break
            if items[index].val == item:
                # check if the input value is repeated
                return False
            if items[index].collision < item_obj.collision:
                temp = items[index]
                items[index] = item_obj
                item_obj = temp
            index = (index + 1) % len(items)
            item_obj.collision += 1
        if location < 0:
            location = index
        items[location] = item_obj
        return True

    @staticmethod
    def __rehash(olditems, newitems):
        for e in olditems:
            if e is not None and type(e) != HashSet.__Placeholder:
                HashSet.__add(e.val, newitems)
        return newitems

    def __contains__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] is not None:
            if type(self.items[index]) != HashSet.__Placeholder:
                if self.items[index].val == item:
                    return True
            index = (index + 1) % len(self.items)
        return False

    def delete(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 20) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None] * (len(self.items) // 2))

    @staticmethod
    def __remove(item, items):
        index = hash(item) % len(items)
        while items[index] is not None:
            if type(items[index]) != HashSet.__Placeholder:
                if items[index].val == item:
                    nextIndex = (index + 1) % len(items)
                    if items[nextIndex] is None:
                        items[index] = None
                    else:
                        items[index] = HashSet.__Placeholder()
                    return True
            index = (index + 1) % len(items)
        return False

    def convert_list(self):
        ans = []
        for i in self.items:
            if i is not None and type(i) != HashSet.__Placeholder :
                ans.append(i.val)
        return ans

    def show(self):
        for item in self.items:
            if item is not None and type(item) != self.__Placeholder:
                assert(type(item) == self.__Item)
                print("(%d, %d)" % (item.val, item.collision), end=" ")

    def union(self, other):
        if type(other) is HashSet:
            other = other.convert_list()
        if type(other) is tuple:
            other = list(other)
        if type(other) is not list:
            raise TypeError("wrong input: only accept lists, tuples or hashset")
        return HashSet(self.convert_list() + other)

    def difference(self, other):
        if type(other) is not HashSet:
            other = HashSet(list(other))
        ans = HashSet(self.convert_list())
        for i in other:
            ans.delete(i)
        return ans

    def intersection(self, other):
        if type(other) is not HashSet:
            other = HashSet(list(other))
        temp = HashSet(self.convert_list())
        diff = temp.difference(other)
        return temp.difference(diff)

content = [21,41,1,61,81,201,101,201,101,21,45,85,61]
test = HashSet(content)
print(test.convert_list())
test.delete(101)
print("\n")
print(test.convert_list())
another = [21,41,1,61,81,201,101,201,101,21,45,85,61,202,15,215,481,101,21,88]
newset = test.union(another)
print(newset.convert_list())
diff = newset.difference(test)
print(newset.convert_list())
print(diff.convert_list())
tointersect = [41,1,61,999]
intersection = newset.intersection(tointersect)
print(intersection.convert_list())