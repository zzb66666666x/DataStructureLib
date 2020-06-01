# this is the exercise 4 of this homework
# this code will generate a perfect match of a biGraph
# this will rely on the algorithm as follows:
# if mode = init
#   then par mode := examine
#           partial match := ∅
#       endpar
# endif
# if mode = examine
#   then if ∃b ∈ Boys.∀g ∈ Girls.{b, g} ∈/ partial match
#       then mode := build-digraph
#   else par Output := true
#       Halt := true
#       mode := final
#       endpar
#   endif
# endif
# if mode = build-digraph
#   then par digraph := girls to boys(partial match)
#                       ∪ boys to girls(E − partial match)
#       mode := build-path
#   endpar
# endif
# if mode = build-path
#   then choose b ∈ {x | x ∈ Boys : ∀g ∈ Girls.{b, g} ∈/ partial match}
#   do if ∃g0 ∈ Girls.∀b0 ∈ Boys.{b0 , g0} ∈/ partial match ∧ reachable(b0, digraph, g0)
#       then choose g ∈ {y | y ∈ Girls.∀x ∈ Boys.{x, y} ∈/ partial match ∧ reachable(b, digraph, y)}
#           do par path := path(b, digraph, g)
#               mode := modify
#           endpar
#           enddo
#   else
#       par Output := false
#       Halt := true
#       mode := final
#       endpar
#   endif
#   enddo
# endif
# if mode = modify
#   then par partial match = (partial match − unordered(path)) ∪ (unordered(path) − partial match)
#       mode := examine
#   endpar
# endif


# The BiGraph contains two sets of vertexes vA & vB
# It is a undirected graph
# It has these methods:
#   addEdge                 add edge to both vertex in vA & vB
#   insertVertexToA         insert vertex to set vA
#   insertVertexToB         insert vertex to set vB
#   deleteVertex            delete vertex from the graph (vA & vB)
#   insertEdge              insert edge and its vertexes into the graph
#   insertEdges             insert edges into the graph
#   deleteEdge              delete edge from the graph
#   outgoingEdges           output a list of outgoing edges of corresponding vertex

#macro definitions
init = 0
examine = 1
final = 2
build_digraph = 3
build_path = 4
modify = 5
Halt = False

class BiGraph:
    # The input of the graph should be an edge (tuple) (A, B)
    # A should be the vertex in set vA or added to A
    # B should be the vertex in set vB or added to B
    # wrong input would break the structure of bipartite graph, which is not acceptable
    def __init__(self, edges=[]):
        self.vA = VertexList()
        self.vB = VertexList()
        for e in edges:
            self.insertEdge(e)

    # iterate edges in vA & vB
    def __iter__(self):
        for v in self.vA:
            x = self.vA.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, z)
        for v in self.vB:
            x = self.vB.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, z)

    # add edge to both vertex in vA & vB (due to the graph is a undirected graph)
    def addEdge(self, edge):
        # Add edge to vertex set A
        vertexA = self.vA.locate(edge[0])
        edgelistA = vertexA.edges
        if edgelistA != None:
            edgelistA.add(edge[1])
        else:
            edgelistA = EdgeList(edge[1])
        vertexA.setEdges(edgelistA)
        # Add edge to vertex set B
        vertexB = self.vB.locate(edge[1])
        edgelistB = vertexB.edges
        if edgelistB != None:
            edgelistB.add(edge[0])
        else:
            edgelistB = EdgeList(edge[0])
        vertexB.setEdges(edgelistB)

    # insert vertex to set vA
    def insertVertexToA(self, item):
        self.vA.addVertex(item)
    # insert vertex to set vB
    def insertVertexToB(self, item):
        self.vB.addVertex(item)

    # delete vertex from the graph (vA & vB)
    def deleteVertex(self, item):
        if item in self.vA:
            self.vB.delEdgeWithItem(item)
            return self.vA.remove(item)
        else:
            self.vA.delEdgeWithItem(item)
            return self.vB.remove(item)

    # The input should be an edge (tuple) (A, B)
    # A should be the vertex in set vA or added to A
    # B should be the vertex in set vB or added to B
    # wrong input would break the structure of bipartite graph, which is not acceptable
    def insertEdge(self, edge):
        if edge[0] in self.vB or edge[1] in self.vA:
            raise Exception("Wrong Input")
        self.vA.addVertex(edge[0])
        self.vB.addVertex(edge[1])
        self.addEdge(edge)

    # The input should be a list consists of edges
    def insertEdges(self,edges):
        for e in edges:
            self.insertEdge(e)

    # delete edge from the graph
    def deleteEdge(self, edge):
        if not (edge[0] in self.vA):
            print("There is no edge", edge)
            return False
        vertexloc = self.vA.locate(edge[0])
        edgelistA = vertexloc.getEdges()
        if edgelistA == None:
            print("There is no edge", edge)
            return False
        res = edgelistA.remove(edge[1])
        if res == False:
            print("There is no edge", edge)
            return res
        if not (edge[1] in self.vB):
            print("There is no edge", edge)
            return False
        vertexloc = self.vB.locate(edge[1])
        edgelistB = vertexloc.getEdges()
        if edgelistB == None:
            print("There is no edge", edge)
            return False
        res = edgelistB.remove(edge[0])
        if res == False:
            print("There is no edge", edge)
        return res

    # output a list of outgoing edges of corresponding vertex
    def outgoingEdges(self, item):
        vertex = self.vA.locate(item)
        if vertex == None:
            vertex = self.vB.locate(item)
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


    def PerfectMatch(self):
        self.Edges = self.__get_all_edges()
        Halt = False
        if self.vA.getlength() != self.vB.getlength():
            return False
        mode = init
        ans = False
        partial_match = set()
        # things stored in partial match: (boy, girl) --> must obey this order
        digraph = DirectedBiGraph()
        path = DirectedBiGraph()
        maximal_loop = 5000
        counter = 0
        while counter < maximal_loop:
            counter += 1
            # print("\n")
            # print("the mode is:", mode)
            # print("partial_match: ",list(partial_match))
            if Halt:
                break
            if mode == init:
                mode = examine
                partial_match = set()
            elif mode == examine:
                # print("judge1 result: ",self.__judge1(partial_match))
                if self.__judge1(partial_match):
                    mode = build_digraph
                else:
                    ans = True
                    mode = final
            elif mode == build_digraph:
                digraph = DirectedBiGraph()
                for pair in partial_match:
                    girls_to_boys = [pair[0],pair[1],1]
                    digraph.insertEdge(girls_to_boys)
                # print("E-partial_match: ", self.Edges - partial_match)
                for pair in (self.Edges - partial_match):
                    boys_to_girls = [pair[0], pair[1], 0]
                    digraph.insertEdge(boys_to_girls)
                # print("    checking the digraph: ")
                # for i in digraph:
                #     print("       ", i)
                # print("    end of checking")
                mode = build_path
            elif mode == build_path:
                boy = self.__judge1_choose(partial_match)
                # print("choose one boy", boy)
                if self.__judge2(partial_match, digraph, boy):
                    girl = self.__judge2_choose(partial_match, digraph, boy)
                    # print("choose one girl: ", girl)
                    path = self.__path(boy, digraph, girl) # the path should be a directed graph
                    mode = modify
                # print("    checking the path: ")
                # for i in path:
                #     print("       ", i)
                # print("    end of checking")
            elif mode == modify:
                unorder = self.__unordered_path(path)
                # print("the unorder: ",unorder)
                partial_match = (partial_match - unorder).union(unorder - partial_match)
                mode = examine
            elif mode == final:
                Halt = True
            else:
                raise Exception("error in the finite state machine")
        if ans:
            return list(partial_match)
        else:
            print("Exceed standard matching time, impossible to find a match.  ", end="")
            return False

    def __get_all_edges(self):
        res = set()
        for v in self.vA:
            x = self.vA.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    res.add((v,z))
        return res

    def __judge1_choose(self, partial_match):
        #choose one with ∃b ∈ Boys.∀g ∈ Girls.{b, g} ∈/ partial match
        return self.__judge1(partial_match, function=1)

    def __judge1(self, partial_match, function=0):
        #∃b ∈ Boys.∀g ∈ Girls.{b, g} ∈/ partial match
        for boy in self.vA:
            test = 1
            for girl in self.vB:
                pair = (boy, girl)
                if pair in partial_match:
                    test = 0
                    break
            if test:
                if function == 0:
                    return True
                else:
                    return boy

    def __judge2_choose(self, partial_match, digraph, boy):
        return self.__judge2(partial_match, digraph, boy, function=1)

    def __judge2(self, partial_match, digraph, start_boy, function=0):
        #∃g0 ∈ Girls.∀b0 ∈ Boys.{b0, g0} ∈ / partial_match ∧ reachable(b0, digraph, g0)
        for girl in self.vB:
            test1 = 1
            test2 = 1
            for boy in self.vA:
                pair = (boy, girl)
                # print("inside the judge2, the pair is: ", pair)
                if pair in partial_match:
                    test1 = 0
                    break
                if self.__reachable(start_boy, digraph, girl):
                    test2 = 1
                    break
                else:
                    test2 = 0
                    continue
            if test1 and test2:
                if function == 0:
                    return True
                else:
                    return girl

    def __reachable(self, boy, digraph, girl):
        path = digraph.dfs(boy,girl)
        if path.empty_graph():
            return False
        return True

    def __path(self, boy, digraph, girl):
        # should return a directed graph which contains the path
        return digraph.dfs(boy, girl)

    def __unordered_path(self, path):
        # the input path is a directed graph
        res = set()
        for i in path:
            boy = i[0]
            girl = i[2]
            res.add((boy, girl))
        return res

class DirectedBiGraph(BiGraph):
    # the edge should look like [vertex1, vertex2, 0 or 1]
    # 0 means vertex1 is starting point
    # 1 means vertex2 is the starting point
    # WARNING: vertex1 belongs to vA and the vertex2 belongs to vB

    # Things remain the same:
    # def outgoingEdges(self, item):

    # def insertVertexToA(self, item):

    # def insertVertexToB(self, item):

    def __init__(self, edges=[]):
        super().__init__(edges)

    # iterate edges in vA & vB
    def __iter__(self):
        for v in self.vA:
            x = self.vA.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, "->",z)
        for v in self.vB:
            x = self.vB.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (z, "<-", v)

    def empty_graph(self):
        total_length = self.vA.getlength() + self.vB.getlength()
        if total_length == 0:
            return True
        return False

    def insertEdge(self, edge):
        if edge[0] not in self.vA:
            self.vA.addVertex(edge[0])
        if edge[1] not in self.vB:
            self.vB.addVertex(edge[1])
        self.addEdge(edge)

    def insertEdges(self,edges):
        for e in edges:
            self.insertEdge(e)

    def addEdge(self, edge):
        if edge[2] == 1:
            # Add edge to vertex set B
            vertexB = self.vB.locate(edge[1])
            edgelistB = vertexB.edges
            if edgelistB != None:
                if edge[0] not in edgelistB:
                    edgelistB.add(edge[0])
            else:
                edgelistB = EdgeList(edge[0])
            vertexB.setEdges(edgelistB)
        else:
            assert(edge[2] == 0)
            vertexA = self.vA.locate(edge[0])
            edgelistA = vertexA.edges
            if edgelistA != None:
                if edge[1] not in edgelistA:
                    edgelistA.add(edge[1])
            else:
                edgelistA = EdgeList(edge[1])
            vertexA.setEdges(edgelistA)

    def dfs(self, root, target):
        # print("inside the dfs")
        # print("    the root is:", root)
        # print("    the target is:", target)
        self.mark = {}
        for i in self.vA:
            self.mark[i] = ["vA", 0]
        for i in self.vB:
            self.mark[i] = ["vB", 0]
        ans = DirectedBiGraph()
        stk = Stack()
        self.__dfs_search(root, target, stk)
        while stk.isEmpty() is False:
            ans.insertEdge(stk.pop())
        return ans

    def __dfs_search(self, root, target, stack):
        if root == target:
            return True
        for e in self.outgoingEdges(root):
            if self.mark[e[1]][1] == 0:
                self.mark[e[1]][1] = 1
                if self.__dfs_search(e[1], target, stack):
                    if self.mark[root][0] == "vA" and self.mark[e[1]][0] == "vB":
                        stack.push([root, e[1], 0])
                    elif self.mark[root][0] == "vB" and self.mark[e[1]][0] == "vA":
                        stack.push([e[1], root, 1])
                    else:
                        raise Exception("something wrong with the input")
                    return True
        return False

    # Things not necessary
    def PerfectMatch(self):
        raise Exception("Don't use this function!!!")

    def deleteEdge(self, edge):
        raise Exception("Don't use this function!!!")

# Definition of VertexList Class
class VertexList:
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

        def setEdges(self, edge):
            self.edges = edge

    def __init__(self, edges=[]):
        self.dummy = VertexList.__Vertex(None, None, None)
        self.numVertices = 0
        self.dummy.setNext(self.dummy)
        self.dummy.setPrevious(self.dummy)
        self.contentSet = set()
        for e in edges:
            self.addVertex(e[0])
            self.addVertex(e[1])

    def addVertex(self, vertex):
        if vertex not in self:
            self.contentSet.add(vertex)
            self.__append(vertex)

    def __iter__(self):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            yield cursor.getItem()

    def __append(self, item):
        lastVertex = self.dummy.getPrevious()
        newVertex = VertexList.__Vertex(item, self.dummy, lastVertex)
        lastVertex.setNext(newVertex)
        self.dummy.setPrevious(newVertex)
        self.numVertices += 1

    def __contains__(self, item):
        if item in self.contentSet:
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

    # if we remove a vertex directly, then the corresponding edgeList will also be influenced
    # so we must:
    # 1. find the item(a vertex here).
    # 2. see if this vertex has many edges from itself:
    #        yes: don't delete it
    #        no: delete it by removing this from the linked list
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

    # delete edges contains corresponding item: edge is a tuple
    # usage: vertexList[xxx].delEdgeWithItem([vertex1, vertex2])
    def delEdgeWithItem(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            edgelist = cursor.edges
            if edgelist != None:
                if item in edgelist:
                    edgelist.remove(item)

    def getlength(self):
        return self.numVertices

    def package(self):
        res = []
        for i in self:
            res.append(i)
        return res

# Definition of EdgeList Class
class EdgeList:
    class __Edge:
        def __init__(self, item, next=None, previous=None):
            self.item = item # this should be a tuple
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

class Stack(object):
    class Node(object):
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self):
        self.head = None

    def top(self):
        if self.head is not None:
            return self.head.val
        else:
            return None

    def push(self, n):
        n = self.Node(n)
        n.next = self.head
        self.head = n
        return n.val

    def pop(self):
        if self.head is None:
            return None
        else:
            tmp = self.head.val
            self.head = self.head.next
            return tmp

    def isEmpty(self):
        if self.head is None:
            return True
        else:
            return False

    def show(self):
        if self.head is None:
            return
        temp = self.head
        while temp is not None:
            temp = temp.next

    def __iter__(self):
        if self.head is None:
            return
        temp = self.head
        while temp is not None:
            yield temp.val
            temp = temp.next


if __name__ == "__main__":
    # test the directed graph
    # digraph = DirectedBiGraph([("b1", "g2", 1),("b1", "g1", 0),("b2", "g2", 0),("b2","g3",0),("b3","g3",0)])
    # for i in digraph:
    #     print(i)
    # print("\n-------\n")
    # # test the path find algorithm
    # path = digraph.dfs("b2", "g1")
    # for i in path:
    #     print(i)
    bigraph1 = BiGraph([("b1", "g3"), ("b2", "g3"), ("b3", "g1"), ("b3", "g2"), ("b2","g2")])
    print(bigraph1.PerfectMatch())
    bigraph2 = BiGraph([("b1", "g2"), ("b1", "g1"), ("b2", "g2")])
    print(bigraph2.PerfectMatch())
    bigraph3 = BiGraph([("b1", "g3"), ("b2", "g3"), ("b3", "g1"), ("b3", "g2")]) # this one don't have a match
    print(bigraph3.PerfectMatch())