class DiGraph:
    def __init__(self, edges=[]):
        self.vertexList = VertexList(edges)
        for e in edges:
            self.addEdge(e)
            ## Modification
            # for directed graph, we only need to store one direction - (in, out)
            # self.addEdge((e[1],e[0]))

    def addEdge(self, edge):
        # locate the related vertex according to the edge given
        vertex = self.vertexList.locate(edge[0])  # edge[0] is the incoming vertex
        edgelist = vertex.edges  # get the edgelist object for this incoming vertex
        if edgelist != None:
            # add outcoming vertex to the edgelist
            edgelist.add(edge[1])
        else:
            # construct a new Edgelist object if this vertex has no edgelist yet
            edgelist = EdgeList(edge[1])
        vertex.setEdges(edgelist)

    def __iter__(self):
        vertices = self.vertexList
        for v in vertices:
            x = vertices.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, z)

    def insertVertex(self, item):
        if not (item in self.vertexList):
            self.vertexList.append(item)

    def deleteVertex(self, item):
        return self.vertexList.remove(item)

    def insertEdge(self, edge):
        self.vertexList.addVertex(edge)
        self.addEdge(edge)
        ## Modification, only one direction now
        # self.addEdge((edge[1],edge[0]))

    def deleteEdge(self, edge):
        self.__deleteEdge(edge)
        ## Modification, only one direction now
        # self.__deleteEdge((edge[1],edge[0]))

    def __deleteEdge(self, edge):
        if not (edge[0] in self.vertexList):
            print("There is no edge", edge)
            return False
        vertexlocation = self.vertexList.locate(edge[0])
        edgelist = vertexlocation.getEdges()
        if edgelist == None:
            print("There is no edge", edge)
            return False
        res = edgelist.remove(edge[1])
        if res == False:
            print("There is no edge", edge)
        return res

    def outgoingEdges(self, item):
        vertex = self.vertexList.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgelist = vertex.getEdges()
        if edgelist == None:
            return []
        res = []
        for v in edgelist:
            res.append((item, v))
        return res
        # yield (item,v) # If we replace the above two lines with this line, then this methods works as an iterator.


# Definition of VertexList Class, a linked list
class VertexList:
    class __Vertex:
        def __init__(self, item, next=None, previous=None):
            self.item = item  # the vertex content
            self.next = next
            self.previous = previous
            self.edges = None  # vertices related to this vertex

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

        def setEdges(self, edge):
            self.edges = edge

    def __init__(self, edges=[]):
        self.dummy = VertexList.__Vertex(None, None, None)
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
        newVertex = VertexList.__Vertex(item, self.dummy, lastVertex)
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

    # locate the vertex location using its vertex value
    def locate(self, vertex):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            item = cursor.getItem()
            if vertex == item:
                return cursor

    # add new vertex if possible for the new edge
    def addVertex(self, edge):
        node1 = edge[0]
        node2 = edge[1]
        if not (node1 in self):
            self.append(node1)
        if not (node2 in self):
            self.append(node2)

    # remove a vertex
    def remove(self, item):
        cursor = self.dummy
        location = None
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            edgelist = cursor.edges
            if edgelist != None:

                if item in edgelist:
                    print(item, "cannot be deleted, as it appears in an edge.")
                    return False
            if vertex == item:
                location = cursor
        if location == None:
            print(item, "is not a vertex.")
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


# Definition of EdgeList Class, also a linked list
class EdgeList:
    class __Edge:
        def __init__(self, item, next=None, previous=None):
            self.item = item
            self.next = next
            self.previous = previous

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

    def __init__(self, edge):
        self.first = EdgeList.__Edge(edge, None, None)
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        self.numEdges = 1

    def add(self, edge):
        lastEdge = self.first.getPrevious()
        newEdge = EdgeList.__Edge(edge, self.first, lastEdge)
        lastEdge.setNext(newEdge)
        self.first.setPrevious(newEdge)
        self.numEdges += 1

    def __iter__(self):
        cursor = self.first
        for i in range(self.numEdges):
            yield cursor.getItem()
            cursor = cursor.getNext()

    def __contains__(self, item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                return True
            cursor = cursor.getNext()
        return False

    def remove(self, item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                nextVertex = cursor.getNext()
                prevVertex = cursor.getPrevious()
                prevVertex.setNext(nextVertex)
                nextVertex.setPrevious(prevVertex)
                self.numEdges -= 1
                if (cursor == self.first):
                    self.first = nextVertex
                return True
            cursor = cursor.getNext()
        return False