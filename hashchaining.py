class HashSetChaining:
    def __init__(self, contents=[], loadMax=0.75, loadMin=0.25):
        self.items = [None] * 20
        self.numItems = 0
        self.loadMax = loadMax
        self.loadMin = loadMin
        for e in contents:
            self.add(e)

    def add(self, item):
        if HashSetChaining.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= self.loadMax:
                self.items = HashSetChaining.__rehash(self.items, [None] * 2 * len(self.items))

    def __contains__(self, item):
        index = hash(item) % len(self.items)
        if self.items[index] == None or type(self.items[index]) == HashSetChaining.__Placeholder:
            return False
        if item in self.items[index]:
            return True
        return False

    def delete(self, item):
        if HashSetChaining.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 20) / len(self.items)
            if load <= self.loadMin:
                self.items = HashSetChaining.__rehash(self.items, [None] * (len(self.items) // 2))
        else:
            raise KeyError("Item not in HashSet")

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
        if items[index] == None:
            items[index] = []
        if item in items[index]:
            return False
        items[index].append(item)
        return True

    @staticmethod
    def __rehash(olditems, newitems):
        for chain in olditems:
            if chain != None and type(chain) != HashSetChaining.__Placeholder:
                for e in chain:
                    HashSetChaining.__add(e, newitems)
        return newitems

    @staticmethod
    def __remove(item, items):
        index = hash(item) % len(items)
        if item in items[index]:
            items[index].remove(item)
            # If the list is empty, replace it with a placeholder
            if items[index] == []:
                items[index] = HashSetChaining.__Placeholder()
            return True
        return False