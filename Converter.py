from asyncio.windows_events import NULL
import queue
import copy
import json

# jsonString = input()
# convertedJson = json.loads(jsonString)

# # Start Copy
# import sys
# import base64
# path = base64.b64decode(sys.argv[1])
# out_file = open(path, "r")
# convertedJson = json.load(out_file)
# out_file.close()
# # End Copy


# def startProcessing(convertedJson):
#     nodes = []
#     edges = []
#     for node in convertedJson["nodes"]:
#         nodes.append(Node(node["name"], node["typeOf"], node["edgeIndices"]))

#     for edge in convertedJson["edges"]:
#         edges.append(Edge(edge["fromNode"], edge["toNode"], edge["input"]))

#     return Convert2DFA(nodes, edges)


class Node:
    def __init__(self, name, typeOf, edgeIndices):
        self.name = name
        self.typeOf = typeOf
        self.edgeIndices = edgeIndices

    def __str__(self):
        return (self.typeOf)


class Edge:
    def __init__(self, fromNode, toNode, input):
        self.fromNode = fromNode
        self.toNode = toNode
        self.input = input


class Path:
    def __init__(self, Cost):
        self.visitedNodes = []
        self.returnedVisitedNodes = []
        self.edgesTaken = []
        self.Cost = Cost

    def __lt__(self, other):
        selfPriority = self.Cost
        otherPriority = other.Cost
        return selfPriority < otherPriority


def Convert2DFA(nodes, edges, Alphabet):
    # global convertedJson
    # startingNode = nodes[convertedJson["startNode"]]
    # startingNode = nodes[0]
    NFA_Table = CreateNFA_Table(nodes, edges, Alphabet)
    DFA_Table = CreateDFA_Table(nodes, edges, Alphabet, NFA_Table)

    return NFA_Table


def CreateNFA_Table(nodes, edges, Alphabet):
    NFA_Table = {}
    # format --> {node1:{input:{node1,node2,...},input2:...etc},node2...}      -- dictionary --> dictionary --> set
    # Creates NFA Table
    for CurrentNode in nodes:
        NFA_Table[CurrentNode.name] = {}
        for alph in Alphabet:
            NFA_Table[CurrentNode.name][alph] = set()

        for edge in CurrentNode.edgeIndices:
            NFA_Table[CurrentNode.name][edges[edge].input].add(
                edges[edge].toNode)

        for alph in Alphabet:
            if NFA_Table[CurrentNode.name][alph] == set():
                NFA_Table[CurrentNode.name][alph] = "Φ"
    return NFA_Table


def CreateDFA_Table(nodes, edges, Alphabet, NFA_Table):
    DFA_Table = {}
    # format --> {node1:{input:({node1,node2,...},GOAL),input2:...etc},node2...}      -- dictionary --> dictionary --> set
    # Creates DFA Table
    startingNode = getEpsilonClosure(NFA_Table, nodes[0].name, nodes)
    tempSet = set()
    NodeStart = repr(startingNode)
    DFA_Table[NodeStart] = {}
    tempTable = {}
    while (DFA_Table != tempTable):
        tempTable = copy.deepcopy(DFA_Table)
        for state in DFA_Table:
            if DFA_Table[state] == {}:
                for alph in Alphabet[:-1]:
                    DFA_Table[NodeStart][alph] = set()
                    for element in eval(NodeStart):
                        DFA_Table[NodeStart][alph].update(
                            NFA_Table[element][alph])

                    for NewState in DFA_Table[NodeStart][alph]:
                        tempSet.update(getEpsilonClosure(
                            NFA_Table, NewState, nodes))
                    DFA_Table[repr(tempSet)] = {}
                    tempSet = set()
            else:
                break

        print(DFA_Table)

    # for edge in CurrentNode.edgeIndices:
    #     NFA_Table[CurrentNode.name][edges[edge].input].add(
    #         edges[edge].toNode)

    # for alph in Alphabet:
    #     if NFA_Table[CurrentNode.name][alph] == set():
    #         NFA_Table[CurrentNode.name][alph] = "Φ"

    return DFA_Table


def getEpsilonClosure(NFA_Table, nodeName, AllNodes):
    EpsilonEquvNodes = NFA_Table[nodeName]["ε"]
    EpsilonEquvNodes.add(nodeName)
    return EpsilonEquvNodes

    # return returnedVisitedNodes
    # return {"visitedNodes": returnedVisitedNodes, "visitedEdges": edgesTaken, "failed": True}


# # Start Copy
# out_file = open(path, "w")
# json.dump(startProcessing(convertedJson), out_file)
# out_file.close()
# End Copy
# print(json.dumps(startProcessing(convertedJson)))

# example
Alphapet = ["a", "b", "ε"]
startingNode = Node(1, "START", [0, 1])
garboNode1 = Node(2, "Normal", [2, 3])
garboNode2 = Node(3, "Normal", [4])
garboNode3 = Node(4, "Normal", [])
garboNode4 = Node(5, "GOAL", [5, 6])
nodes = [startingNode, garboNode1, garboNode2, garboNode3, garboNode4]

edge0 = Edge(1, 2, "ε")
edge1 = Edge(1, 3, "a")
edge2 = Edge(2, 5, "a")
edge3 = Edge(2, 4, "a")
edge4 = Edge(3, 4, "b")
edge5 = Edge(5, 4, "a")
edge6 = Edge(5, 4, "b")
edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6]

answer = Convert2DFA(nodes, edges, Alphapet)
print(answer)

# example2
# startingnode = Node("START",1,0,[0])
# garbonode1 = Node ("Normal",1,0,[1,2])
# garbonode2 = Node ("Normal",2,0,[3])
# garbonode3 = Node ("Normal",3,0,[4])
# goalnode = Node("GOAL",0,0,[])
# nodes = [startingnode, garbonode1,garbonode2,garbonode3, goalnode]

# edge0 = Edge(0,1,True,1)
# edge1 = Edge(1,4,True,8)
# edge2 = Edge(1,2,True,1)
# edge3 = Edge(2,3,True,1)
# edge4 = Edge(3,1,True,1)
# edges = [edge0,edge1,edge2,edge3,edge4]

# answer = UCS(nodes,edges)

# example3
# startingNode = Node("START",4,0,[0])
# garboNode1 = Node ("Normal",2,0,[0,1,2])
# garboNode2 = Node ("Normal",1,0,[1,3])
# goalNode = Node("GOAL",0,0,[2,3])
# nodes = [startingNode, garboNode1,garboNode2, goalNode]

# edge0 = Edge(0,1,False,1)
# edge1 = Edge(1,2,False,1)
# edge2 = Edge(1,3,False,3)
# edge3 = Edge(2,3,False,2)
# edges = [edge0,edge1,edge2,edge3]

# answer = UCS(nodes,edges)

# example4
# startingNode = Node("START",1,0,[0,1,2,3])
# garboNode1 = Node ("Normal",1,0,[4])
# garboNode2 = Node ("Normal",2,0,[5])
# garboNode3 = Node ("Normal",3,0,[6])
# garboNode4 = Node ("Normal",4,0,[7])
# goalNode = Node("GOAL",0,0,[])
# nodes = [startingNode, garboNode1,garboNode2,garboNode3,garboNode4, goalNode]

# edge0 = Edge(0,1,True,1)
# edge1 = Edge(0,2,True,2)
# edge2 = Edge(0,3,True,3)
# edge3 = Edge(0,4,True,4)
# edge4 = Edge(1,5,True,1)
# edge5 = Edge(2,5,True,2)
# edge6 = Edge(3,5,True,3)
# edge7 = Edge(4,5,True,4)
# edges = [edge0,edge1,edge2,edge3,edge4,edge5,edge6,edge7]

# answer = UCS(nodes,edges)

# example5
# startingNode = Node("START",1,0,[0])
# garboNode1 = Node ("Normal",1,0,[1])
# garboNode2 = Node ("Normal",2,0,[2])
# nodes = [startingNode, garboNode1,garboNode2]

# edge0 = Edge(0,1,True,1)
# edge1 = Edge(1,2,True,1)
# edge2 = Edge(2,0,True,1)
# edges = [edge0,edge1,edge2]

# answer = UCS(nodes,edges)
