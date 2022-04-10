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

debugger = 0


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

    return NFA_Table, DFA_Table


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
    DFA_Table[repr(startingNode)] = {}
    tempTable = {}
    while (DFA_Table != tempTable):
        tempTable = copy.deepcopy(DFA_Table)
        for state in tempTable:
            if (debugger == 1):
                print("in state for loop", DFA_Table)
            if DFA_Table[state] == {} and state != "Φ":
                for alph in Alphabet[:-1]:
                    if (debugger == 1):
                        print("in alph for loop", DFA_Table)
                    DFA_Table[state][alph] = set()
                    for element in eval(state):
                        DFA_Table[state][alph].update(
                            NFA_Table[element][alph])
                        if (debugger == 1):
                            print("in eval for loop", DFA_Table)
                    if (DFA_Table[state][alph] != {"Φ"}):
                        DFA_Table[state][alph].discard("Φ")
                        for NewState in DFA_Table[state][alph]:
                            tempSet.update(getEpsilonClosure(
                                NFA_Table, NewState, nodes))
                        if (repr(tempSet) not in DFA_Table):
                            DFA_Table[repr(tempSet)] = {}
                        if (debugger == 1):
                            print("in new state for loop", DFA_Table)
                    else:
                        DFA_Table["Φ"] = {}
                    tempSet = set()
            elif state == "Φ":
                for alph in Alphabet[:-1]:
                    DFA_Table[state][alph] = set({"Φ"})
        if (debugger == 1):
            print(DFA_Table)

    # for edge in CurrentNode.edgeIndices:
    #     NFA_Table[CurrentNode.name][edges[edge].input].add(
    #         edges[edge].toNode)

    # for alph in Alphabet:
    #     if NFA_Table[CurrentNode.name][alph] == set():
    #         NFA_Table[CurrentNode.name][alph] = "Φ"

    return DFA_Table


def getEpsilonClosure(NFA_Table, nodeName, AllNodes):
    EpsilonEquvNodes = set()
    EpsilonEquvNodes.update(NFA_Table[nodeName]["ε"])
    EpsilonEquvNodes.add(nodeName)
    EpsilonEquvNodes.discard("Φ")
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
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1])
# garboNode1 = Node(2, "Normal", [2, 3])
# garboNode2 = Node(3, "Normal", [4])
# garboNode3 = Node(4, "Normal", [])
# garboNode4 = Node(5, "GOAL", [5, 6])
# nodes = [startingNode, garboNode1, garboNode2, garboNode3, garboNode4]

# edge0 = Edge(1, 2, "ε")
# edge1 = Edge(1, 3, "a")
# edge2 = Edge(2, 5, "a")
# edge3 = Edge(2, 4, "a")
# edge4 = Edge(3, 4, "b")
# edge5 = Edge(5, 4, "a")
# edge6 = Edge(5, 4, "b")
# edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6]

# answer = Convert2DFA(nodes, edges, Alphapet)
# print(answer[0], "\n \n \n", answer[1])

# example2
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1, 2])
# garboNode4 = Node(2, "GOAL", [3, 4, 5])
# nodes = [startingNode, garboNode4]

# edge0 = Edge(1, 2, "a")
# edge1 = Edge(1, 1, "a")
# edge2 = Edge(1, 1, "b")
# edge3 = Edge(2, 2, "a")
# edge4 = Edge(2, 2, "b")
# edge5 = Edge(2, 1, "b")
# edges = [edge0, edge1, edge2, edge3, edge4, edge5]

# answer = Convert2DFA(nodes, edges, Alphapet)
# print(answer[0], "\n \n \n", answer[1])

# example3
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1, 2])
# garboNode1 = Node(2, "NORMAL", [3])
# garboNode2 = Node(3, "GOAL", [])
# nodes = [startingNode, garboNode1, garboNode2]

# edge0 = Edge(1, 1, "a")
# edge1 = Edge(1, 1, "b")
# edge2 = Edge(1, 2, "a")
# edge3 = Edge(2, 3, "b")
# edges = [edge0, edge1, edge2, edge3]

# answer = Convert2DFA(nodes, edges, Alphapet)
# print(answer[0], "\n \n \n", answer[1])

# example4
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0])
# garboNode1 = Node(2, "NORMAL", [1, 2])
# garboNode2 = Node(3, "GOAL", [3, 4, 5])
# garboNode3 = Node(4, "NORMAL", [6])
# nodes = [startingNode, garboNode1, garboNode2, garboNode3]

# edge0 = Edge(1, 4, "a")
# edge1 = Edge(2, 2, "b")
# edge2 = Edge(2, 3, "a")
# edge3 = Edge(3, 1, "b")
# edge4 = Edge(3, 4, "a")
# edge5 = Edge(3, 4, "b")
# edge6 = Edge(4, 3, "b")

# edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6]

# answer = Convert2DFA(nodes, edges, Alphapet)
# print(answer[0], "\n \n \n", answer[1])

# example5
Alphapet = ["a", "b", "ε"]
startingNode = Node(1, "START", [0])
garboNode1 = Node(2, "NORMAL", [1, 2, 3])
garboNode2 = Node(3, "GOAL", [4])
garboNode3 = Node(4, "GOAL", [5, 6])
nodes = [startingNode, garboNode1, garboNode2, garboNode3]

edge0 = Edge(1, 2, "ε")
edge1 = Edge(2, 1, "b")
edge2 = Edge(2, 2, "a")
edge3 = Edge(2, 3, "a")
edge4 = Edge(3, 4, "b")
edge5 = Edge(4, 1, "a")
edge6 = Edge(4, 4, "a")

edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6]

answer = Convert2DFA(nodes, edges, Alphapet)
print(answer[0], "\n \n \n", answer[1])

# example6
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1])
# garboNode1 = Node(2, "GOAL", [2, 3])
# garboNode2 = Node(3, "NORMAL", [4])
# garboNode3 = Node(4, "GOAL", [5, 6])
# garboNode4 = Node(5, "NORMAL", [7, 8])
# nodes = [startingNode, garboNode1, garboNode2, garboNode3, garboNode4]

# edge0 = Edge(1, 1, "b")
# edge1 = Edge(1, 2, "a")
# edge2 = Edge(2, 2, "a")
# edge3 = Edge(2, 3, "ε")
# edge4 = Edge(3, 4, "b")
# edge5 = Edge(4, 3, "a")
# edge6 = Edge(4, 2, "a")
# edge7 = Edge(5, 1, "b")
# edge8 = Edge(5, 4, "a")

# edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8]

# answer = Convert2DFA(nodes, edges, Alphapet)
# print(answer[0], "\n \n \n", answer[1])

# example7
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1, 2])
# garboNode1 = Node(2, "NORMAL", [3, 4, 5])
# garboNode2 = Node(3, "GOAL", [6, 7, 8, 9])
# nodes = [startingNode, garboNode1, garboNode2]

# edge0 = Edge(1, 2, "a")
# edge1 = Edge(1, 2, "b")
# edge2 = Edge(1, 3, "b")
# edge3 = Edge(2, 1, "b")
# edge4 = Edge(2, 3, "a")
# edge5 = Edge(2, 3, "b")
# edge6 = Edge(3, 1, "a")
# edge7 = Edge(3, 1, "b")
# edge8 = Edge(3, 2, "a")
# edge9 = Edge(3, 2, "b")

# edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8, edge9]

# answer = Convert2DFA(nodes, edges, Alphapet)
# print(answer[0], "\n \n \n", answer[1])
