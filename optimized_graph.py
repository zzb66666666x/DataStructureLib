# this new graph can save space for the graph representation
# this code is from lab, not for HW7

class Graph_M:
    def __init__(self, edges=[]):
        self.vertexList = VertexList_M(edges)
        self.edgeList = None
        for e in edges:
            self.addEdge(e)
        # Set the pointer to edge lists for each vertex
        cursor = self.vertexList.dummy
        length = self.vertexList.getlength()
        for i in range(length):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            try:
                cursor.setEdges(self.edgeList.vertexMap[vertex])
            except KeyError:
                cursor.setEdges(None)

    def addEdge(self, edge):
        if self.edgeList != None:
            self.edgeList.add(edge)
        else:
            self.edgeList = EdgeList_M(edge)

    def __iter__(self):
        for edge in self.edgeList:
            yield edge

    def insertVertex(self, item):
        if not (item in self.vertexList):
            self.vertexList.append(item)

    def deleteVertex(self, item):
        return self.vertexList.remove(item)

    def insertEdge(self, edge):
        # Check if the vertices exist before insertion
        update = [0, 0]
        if not (edge[0] in self.vertexList):
            update[0] = 1
        if not (edge[1] in self.vertexList):
            update[1] = 1
        self.vertexList.addVertex(edge)
        self.addEdge(edge)
        # Update edge lists
        if update[0] == 1:
            cursor = self.vertexList.locate(edge[0])
            cursor.setEdges(self.edgeList.vertexMap[edge[0]])
        if update[1] == 1:
            cursor = self.vertexList.locate(edge[1])
            cursor.setEdges(self.edgeList.vertexMap[edge[1]])

    def deleteEdge(self, edge):
        self.__deleteEdge(edge)

    def __deleteEdge(self, edge):
        if not (edge[0] in self.vertexList):
            print("1There is no edge", edge)
            return False
        if not (edge[1] in self.vertexList):
            print("2There is no edge", edge)
            return False
        vertexlocation = self.vertexList.locate(edge[0])
        edgeFirst = vertexlocation.getEdges()
        if edgeFirst == None:
            print("3There is no edge", edge)
            return False
        vertexlocation = self.vertexList.locate(edge[1])
        edgeFirst = vertexlocation.getEdges()
        if edgeFirst == None:
            print("4There is no edge", edge)
            return False
        res = self.edgeList.remove(edge)
        if res == False:
            print("There is no edge", edge)
        elif res == 1:
            self.deleteVertex(edge[0])
        elif res == 2:
            self.deleteVertex(edge[1])
        elif res == 3:
            self.deleteVertex(edge[0])
            self.deleteVertex(edge[1])
        # Update edge lists
        vertexlocation = self.vertexList.locate(edge[0])
        try:
            vertexlocation.setEdges(self.edgeList.vertexMap[edge[0]])
        except KeyError:
            vertexlocation.setEdges(None)
        vertexlocation = self.vertexList.locate(edge[1])
        try:
            vertexlocation.setEdges(self.edgeList.vertexMap[edge[1]])
        except KeyError:
            vertexlocation.setEdges(None)
        return res

    def outgoingEdges(self, item):
        vertex = self.vertexList.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgeFirst = vertex.getEdges()
        if edgeFirst == None:
            return []
        res = []
        flag = 0
        cursor = edgeFirst
        while (flag == 0 or (flag == 1 and cursor != edgeFirst)):
            if flag == 0:
                flag = 1
            edge = cursor.getItem()
            if edge[0] != item:
                edge = (edge[1], edge[0])
            res.append(edge)
            cursor = cursor.getNext(item)
        return res
        # yield (item,v) # If we replace the above two lines with this line, then this methods works as an iterator.

    def incomingEdges(self, item):
        vertex = self.vertexList.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgeFirst = vertex.getEdges()
        if edgeFirst == None:
            return []
        res = []
        flag = 0
        cursor = edgeFirst
        while (flag == 0 or (flag == 1 and cursor != edgeFirst)):
            if flag == 0:
                flag = 1
            edge = cursor.getItem()
            if edge[1] != item:
                edge = (edge[1], edge[0])
            res.append(edge)
            cursor = cursor.getNext(item)
        return res


# Modified VertexList Class
class VertexList_M:
    class __Vertex:
        def __init__(self, item, next=None, previous=None):
            self.item = item
            self.next = next
            self.previous = previous
            self.edges = None

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def getEdges(self):
            return self.edges

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

        def setEdges(self, edges):
            self.edges = edges

    def __init__(self, edges=[]):
        self.dummy = VertexList_M.__Vertex(None, None, None)
        self.numVertices = 0
        self.dummy.setNext(self.dummy)
        self.dummy.setPrevious(self.dummy)
        for e in edges:
            self.addVertex(e)

    def __iter__(self):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            yield cursor.getItem()

    def append(self, item):
        lastVertex = self.dummy.getPrevious()
        newVertex = VertexList_M.__Vertex(item, self.dummy, lastVertex)
        lastVertex.setNext(newVertex)
        self.dummy.setPrevious(newVertex)
        self.numVertices += 1

    def __contains__(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            if vertex == item:
                return True
        return False

    def locate(self, vertex):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            item = cursor.getItem()
            if vertex == item:
                return cursor
        return None

    def addVertex(self, edge):
        node1 = edge[0]
        node2 = edge[1]
        if not (node1 in self):
            self.append(node1)
        if not (node2 in self):
            self.append(node2)

    def remove(self, item):
        location = self.locate(item)
        if location == None:
            print(item, "is not a vertex.")
            return False
        edgeFirst = location.edges
        if edgeFirst != None:
            print(item, "cannot be deleted, as it appears in an edge.")
            return False
        nextVertex = location.getNext()
        prevVertex = location.getPrevious()
        prevVertex.setNext(nextVertex)
        nextVertex.setPrevious(prevVertex)
        self.numVertices -= 1
        return True

    def index(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            if cursor.getItem() == item:
                return i
        return -1

    def getlength(self):
        return self.numVertices


# Modified EdgeList Class
class EdgeList_M:
    class __Edge:
        def __init__(self, item1, item2, next1=None, previous1=None, next2=None, previous2=None):
            self.item1 = item1
            self.item2 = item2
            self.next1 = next1  # Outgoing
            self.previous1 = previous1  # Incoming
            self.next2 = next2
            self.previous2 = previous2

        def getItem(self):
            return (self.item1, self.item2)

        def getNext(self, item):
            if item == self.item1:
                return self.next1
            elif item == self.item2:
                return self.next2
            else:
                raise ValueError("Item not in edge")

        def getPrevious(self, item):
            if item == self.item1:
                return self.previous1
            elif item == self.item2:
                return self.previous2
            else:
                raise ValueError("Item not in edge")

        def setItem1(self, item):
            self.item1 = item

        def setItem2(self, item):
            self.item2 = item

        def setNext(self, next, item):
            if item == self.item1:
                self.next1 = next
            elif item == self.item2:
                self.next2 = next
            else:
                raise ValueError("Item not in edge")

        def setPrevious(self, previous, item):
            if item == self.item1:
                self.previous1 = previous
            elif item == self.item2:
                self.previous2 = previous
            else:
                raise ValueError("Item not in edge")

    def __init__(self, edge):
        newEdge = EdgeList_M.__Edge(edge[0], edge[1], None, None, None, None)
        newEdge.setNext(newEdge, edge[0])
        newEdge.setNext(newEdge, edge[1])
        newEdge.setPrevious(newEdge, edge[0])
        newEdge.setPrevious(newEdge, edge[1])
        self.numEdges = 1
        self.vertexMap = {edge[0]: newEdge, edge[1]: newEdge}  # Provides the first edge that each vertex points to

    def add(self, edge):
        newEdge = EdgeList_M.__Edge(edge[0], edge[1], None, None, None, None)
        # Check if edge[0] exists in other edges
        try:
            edgeFirst = self.vertexMap[edge[0]]
            edgePrev = edgeFirst.getPrevious(edge[0])
            edgePrev.setNext(newEdge, edge[0])
            newEdge.setPrevious(edgePrev, edge[0])
            newEdge.setNext(edgeFirst, edge[0])
            edgeFirst.setPrevious(newEdge, edge[0])
        except KeyError:
            newEdge.setNext(newEdge, edge[0])
            newEdge.setPrevious(newEdge, edge[0])
            self.vertexMap[edge[0]] = newEdge
        # Check if edge[1] exists in other edges
        try:
            edgeFirst = self.vertexMap[edge[1]]
            edgePrev = edgeFirst.getPrevious(edge[1])
            edgePrev.setNext(newEdge, edge[1])
            newEdge.setPrevious(edgePrev, edge[1])
            newEdge.setNext(edgeFirst, edge[1])
            edgeFirst.setPrevious(newEdge, edge[1])
        except KeyError:
            newEdge.setNext(newEdge, edge[1])
            newEdge.setPrevious(newEdge, edge[1])
            self.vertexMap[edge[1]] = newEdge
        self.numEdges += 1

    def __iter__(self):
        for item in self.vertexMap.keys():
            cursorFirst = self.vertexMap[item]
            cursor = cursorFirst
            flag = 0
            while (flag == 0 or (flag == 1 and cursor != cursorFirst)):
                if flag == 0:
                    flag = 1
                edge = cursor.getItem()
                if edge[0] != item:
                    edge = (edge[1], edge[0])
                yield edge
                cursor = cursor.getNext(item)

    def __contains__(self, item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                return True
            cursor = cursor.getNext()
        return False

    def remove(self, edge):
        ret = 4
        # edge[0] cursor
        cursorFirst = self.vertexMap[edge[0]]
        cursor = cursorFirst
        flag = 0
        find_flag = 0
        while (flag == 0 or (flag == 1 and cursor != cursorFirst)):
            if flag == 0:
                flag = 1
            edge_t = cursor.getItem()
            if edge_t == edge or (edge_t[1], edge_t[0]) == edge:
                find_flag = 1
                cursorNext = cursor.getNext(edge[0])
                if cursor == cursorFirst:
                    self.vertexMap[edge[0]] = cursorNext
                    if self.vertexMap[edge[0]] == cursorFirst:
                        del self.vertexMap[edge[0]]
                        ret += 1
                        break
                cursorPrev = cursor.getPrevious(edge[0])
                cursorPrev.setNext(cursorNext, edge[0])
                cursorNext.setPrevious(cursorPrev, edge[0])
                break
            cursor = cursor.getNext(edge[0])
        if find_flag == 0:
            return False
        # edge[1] cursor
        cursorFirst = self.vertexMap[edge[1]]
        cursorNext = cursor.getNext(edge[1])
        if cursor == cursorFirst:
            self.vertexMap[edge[1]] = cursorNext
            if self.vertexMap[edge[1]] == cursorFirst:
                del self.vertexMap[edge[1]]
                ret += 2
        cursorPrev = cursor.getPrevious(edge[1])
        cursorPrev.setNext(cursorNext, edge[1])
        cursorNext.setPrevious(cursorPrev, edge[1])
        return ret