# Universal 1-hashing
"""
Created on Fri Mar 27 20:15:06 2020

@author: zzb
"""
import numpy as np
import math
class HashSet:
    
    ## Define you new hash function here
    def __hash(self, elem):
        sum_product = 0
        flag = self.flag
        digits = []
        while elem != 0:
            temp = flag & elem
            digits.append(temp)
            elem = elem>>self.w
        for i in range(len(digits)):
            sum_product += (digits[i]*self.a[i])
        return sum_product % self.size
        
    def __init__(self,contents=[]):
        self.items = [None] * 17
        self.size = 17
        # add w & a here
        # calculate word length w here
        self.w = math.floor(math.log(self.size, 2))
        temp = 1
        temp_sum = 0
        for i in range(self.w):
            temp_sum += temp
            temp = temp<<1
        self.flag = temp_sum
        self.k = math.ceil(128/self.w)
        # generate one random hash function
        self.a = tuple(np.random.randint(0,self.size, self.k))
        self.numItems = 0
        for e in contents:
            self.add(e)
            
    def add(self,item):
        if HashSet.__add(self, item,self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self, self.items, [None]*2*len(self.items))
                
    def __contains__(self,item):
#         index = hash(item) % len(self.items)
        index = self.__hash(item)
        while self.items[index] != None:
            if self.items[index] == item:
                return True
            index = (index + 1) % len(self.items)
        return False
    
    def delete(self,item):
        if HashSet.__remove(self,item,self.items):
            self.numItems -= 1
            load = max(self.numItems,20) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self, self.items, [None]*(len(self.items) // 2))
        else:
            raise KeyError("Item not in HashSet")

    # ===== Hidden Class =====
    class __Placeholder:
        def __init__(self):
            pass
        
        def __eq__(self,other):
            return False
    
    # ===== Auxiliary Functions =====
    # They all have '__' as prefixes to indicate that they are private methods to the class
    def __add(self, item,items):
        index = self.__hash(item) # hash() is used to produce a number for item
        location = -1
        pt_test = 0
        while items[index] != None:
            if items[index] == item:
                return False
            if location < 0 and type(items[index]) == HashSet.__Placeholder:
                location = index
            index = (index + 1) % len(items)
            pt_test = 1
        if location < 0:
            location = index
        items[location] = item
        return True
        
    def __rehash(self, olditems,newitems):
    ## Modify here
        # update p, w, and a
        self.size = len(newitems) # A relaxed method
        self.w = math.floor(math.log(self.size, 2))
        self.k = math.ceil(128/self.w)
        self.a = tuple(np.random.randint(0,self.size,self.k))
        temp = 1
        temp_sum = 0
        for i in range(self.w):
            temp_sum += temp
            temp = temp<<1
        self.flag = temp_sum
        self.items = newitems
        for e in olditems:
            if type(e) == int or type(e) == tuple:
                HashSet.__add(self, e,newitems)
        return newitems
                
    def __remove(self, item,items):
        index = self.__hash(item)
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


a = [11,12,3666,9,4,1,8,1,5,7,4,5,5555,88,9,666663,1,4452145,5412,264126]
hs = HashSet(a)
for i in hs.items:
    print(i)