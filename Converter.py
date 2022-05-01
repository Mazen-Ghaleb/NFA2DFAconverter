# from asyncio.windows_events import NULL
# from automathon import DFA
import queue
import copy
import json
import numpy as np
from os import system

# Copied from automathon
class Error(Exception):
  """Base class for exceptions in this module."""
  pass

class InputError(Error):
  """Exception raised for errors in the input.

  Attributes
  - - - - - - - - - - - - - - - - - -

    expression : str
      Input expression in which the error ocurred.

    message : str
      Explaination of the error.
  """

  def __init__(self, expression, message):
    self.expression = expression
    self.message = message


class SigmaError(Error):
  """Exception raised for errors in the transition.

  Attributes
  - - - - - - - - - - - - - - - - - -

    expression : str
      Input expression in which the error ocurred.

    message : str
      Explaination of the error.
  """

  def __init__(self, expression, message):
    self.expression = expression
    self.message = message


class DFA:
  """A Class used to represent a Deterministic Finite Automaton

  ...

  Attributes
  - - - - - - - - - - - - - - - - - -
  Q : set
    Set of strings where each string represent the states.
    Ex:
      Q = {'q0', 'q1', 'q2'}

  sigma : set
    Set of strings that represents the alphabet.
    Ex:
      sigma = {'0', '1'}
  
  delta : dict
    Dictionary that represents the transition function.
    Ex:
      delta = {
                'q0' : {'0' : 'q0', '1' : 'q1'},
                'q1' : {'0' : 'q2', '1' : 'q0'},
                'q2' : {'0' : 'q1', '1' : 'q2'},
              }
  
  initialState : str
    String that represents the initial state from where any input is processed (initialState ∈ Q / initialState in Q).
    Ex:
      initialState = 'q0'
  
  F : set
    Set of strings that represent the final state/states of Q (F ⊆ Q).
    Ex:
      F = {'q0'}
  

  Methods
  - - - - - - - - - - - - - - - - - -

  isValid() -> bool : Returns True if the DFA is a valid automata
  accept(S : str) -> bool : Returns True if the given string S is accepted by the DFA
  complement() -> DFA : Returns the complement of the DFA
  """
  
  def __init__(self, Q: set, sigma: set, delta: dict, initialState: str, F: set):
    """
    Parameters
    - - - - - - - - - - - - - - - - - -
    
    Q : set
      Set of strings where each string represent the states.
    
    sigma : set
      Set of strings that represents the alphabet.
    
    delta : dict
      Dictionary that represents the transition function.
    
    initialState : str
      String that represents the initial state from where any input is processed (initialState ∈ Q / initialState in Q).
    
    F : set
      Set of strings that represent the final state/states of Q (F ⊆ Q).
    """
    self.Q = Q
    self.sigma = sigma
    self.delta = delta
    self.initialState = initialState
    self.F = F
  
  def accept(self, S: str) -> bool:
    """ Returns True if the given string S is accepted by the DFA

    The string S will be accepted if ∀a · a ∈ S ⇒ a ∈ sigma, which means that all the characters in S must be in sigma (must be in the alphabet).

    Parameters
    - - - - - - - - - - - - - - - - - -
    S : str
      A string that the DFA will try to process.
    """
    
    ## Basic Idea: Search through states (delta) in the DFA, since the initial state to the final states
    
    ## BFS states
    
    q = deque()  ## queue -> states from i to last character in S | (index, state)
    q.append([0, self.initialState])  ## Starts from 0
    ans = False  ## Flag
    
    while q and not ans:
      frontQ = q.popleft()
      idx = frontQ[0]
      state = frontQ[1]
      
      if idx == len(S):
        if state in self.F:
          ans = True
      elif S[idx] not in self.sigma:
        raise InputError(S[idx], 'Is not declared in sigma')
      elif state in self.delta:
        ## Search through states
        for transition in self.delta[state].items():
          ## transition = ('1', 'q0')
          if S[idx] == transition[0]:
            q.append([idx + 1, transition[1]])
    
    if S == "":
      ans = True
    
    return ans
  
  def isValid(self) -> bool:
    """ Returns True if the DFA is an valid automata """
    
    # Validate if the initial state is in the set Q
    if self.initialState not in self.Q:
      raise SigmaError(self.initialState, 'Is not declared in Q')
    
    # Validate if the delta transitions are in the set Q
    for d in self.delta:
      if d not in self.Q:
        raise SigmaError(d, 'Is not declared in Q')
      
      # Validate if the d transitions are valid
      for s in self.delta[d]:
        if s not in self.sigma:
          raise SigmaError(s, 'Is not declared in sigma')
        elif self.delta[d][s] not in self.Q:
          raise SigmaError(self.delta[d][s], 'Is not declared Q')
    
    # Validate if the final state are in Q
    for f in self.F:
      if f not in self.Q:
        raise SigmaError(f, 'Is not declared in Q')
    
    # None of the above cases failed then this DFA is valid
    return True
  
  def complement(self) -> 'DFA':
    """Returns the complement of the DFA."""
    Q = self.Q
    sigma = self.sigma
    delta = self.delta
    initialState = self.initialState
    F = {state for state in self.Q if state not in self.F}
    
    return DFA(Q, sigma, delta, initialState, F)
  
  def getNFA(self):
    from automathon.finiteAutomata.nfa import NFA
    """Convert the actual DFA to NFA class and return it's conversion"""
    Q = self.Q.copy()
    delta = dict()
    initialState = self.initialState
    F = self.F.copy()
    sigma = self.sigma
    
    for state, transition in self.delta.items():
      ## state : str, transition : dict(sigma, Q)
      tmp = dict()
      for s, q in transition.items():
        ## s : sigma
        tmp[s] = [''.join(q)]
      
      delta[state] = tmp
    
    return NFA(Q, sigma, delta, initialState, F)
  
  def product(self, M: 'DFA') -> 'DFA':
    """Given a DFA M returns the product automaton"""
    delta = dict()
    Q = set()
    F = set()
    sigma = self.sigma.intersection(M.sigma)
    
    for state, transition in self.delta.items():
      ## i : str, j : dict(sigma, Q)
      for stateM, transitionM in M.delta.items():
        ## stateM : str, transitionM : dict(sigma, Q)
        for s in transition:
          if s in transitionM:
            ## sigma value in common
            sigma.add(s)
            
            tmp = str([state, stateM])
            tmp1 = str([transition[s], transitionM[s]])
            aux = dict()
            aux[s] = tmp1
            
            Q.add(tmp)
            Q.add(tmp1)
            
            if state in self.F and stateM in M.F:
              F.add(tmp)
            
            if transition[s] in self.F and transitionM[s] in M.F:
              F.add(tmp1)
            
            if tmp in delta:
              delta[tmp].update(aux)
            else:
              delta[tmp] = aux
    
    return DFA(Q, sigma, delta, str([self.initialState, M.initialState]), F)
  
  def union(self, M: 'DFA') -> 'DFA':
    """Given a DFA M returns the union automaton"""
    tmpNFA = self.getNFA()
    tmpNFA = tmpNFA.union(M.getNFA()).removeEpsilonTransitions()
    
    return tmpNFA.getDFA()
  
  def view(self, fileName: str):
    dot = Digraph(name=fileName, format='png')
    
    dot.graph_attr['rankdir'] = 'LR'
    
    dot.node("", "", shape='plaintext')
    
    for f in self.F:
      dot.node(f, f, shape='doublecircle')
    
    for q in self.Q:
      if q not in self.F:
        dot.node(q, q, shape='circle')
    
    dot.edge("", self.initialState, label="")
    
    for q in self.delta:
      for s in self.delta[q]:
        dot.edge(q, self.delta[q][s], label=s)
    
    dot.render()

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

def startProcessing(convertedJson):
    nodes = []
    edges = []
    
    for node in convertedJson["nodes"]:
        nodes.append(Node(node["name"], node["typeOf"], node["edgeIndices"]))

    for edge in convertedJson["edges"]:
        edges.append(Edge(edge["fromNode"], edge["toNode"], edge["input"]))
    
    Alphabet = convertedJson["alphabet"]
    startNode = convertedJson["startNode"]
    mode = convertedJson["mode"]

    Result = Convert2DFA(nodes ,edges, Alphabet , startNode , mode)


#Variable to help in debugging
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


def Convert2DFA(nodes, edges, Alphabet ,startNode , mode):
    # mode false to not show epsilon closure in transitions , and true to show it
    # global convertedJson
    # startingNode = nodes[convertedJson["startNode"]]
    # startingNode = nodes[0]
    FinalNodes = getFinalNodes(nodes, edges)
    NFA_Table = CreateNFA_Table(nodes, edges, Alphabet)
    DFA_Table ,DFA_Start = CreateDFA_Table(nodes, edges, Alphabet,startNode, NFA_Table,mode)
    DFA_Structure ,DFA_Final = getDFA_Structure(DFA_Table, FinalNodes)

    #print(set(DFA_Structure.keys()),Alphabet[:-1], DFA_Structure,DFA_Start ,DFA_Final)
    automata1 = DFA(set(DFA_Structure.keys()),Alphabet[:-1], DFA_Structure,DFA_Start ,DFA_Final)
    print(automata1.isValid())
    system("pwd")
    # automata1.view("DFA.png")
    view(automata1, "DFA.png")
    
    return NFA_Table,DFA_Structure

from graphviz import Digraph
def view(self, fileName: str):
    dot = Digraph(name=fileName)
    
    dot.graph_attr['rankdir'] = 'LR'
    
    dot.node("", "", shape='plaintext')
    
    for f in self.F:
      dot.node(f, f, shape='doublecircle')
    
    for q in self.Q:
      if q not in self.F:
        dot.node(q, q, shape='circle')
    
    dot.edge("", self.initialState, label="")
    
    for q in self.delta:
      for s in self.delta[q]:
        dot.edge(q, self.delta[q][s], label=s)
    
    print(dot.source)
    # dot.render()

def getFinalNodes(nodes, edges):
    FinalNodes = set()
    for CurrentNode in nodes:
        if CurrentNode.typeOf == "FINAL":
            FinalNodes.add(CurrentNode.name)
    return FinalNodes


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


def CreateDFA_Table(nodes, edges, Alphabet,startNode, NFA_Table,mode):
    # format --> {node1:{input:{node1,node2,...},input2:...etc},node2...}      -- dictionary --> dictionary --> set
    # Creates DFA Table
    DFA_Table = {}
    startingNode = getEpsilonClosure(NFA_Table, nodes[startNode].name)
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
                        DFA_Table[state][alph] = set(sorted(DFA_Table[state][alph]))
                        for NewState in DFA_Table[state][alph]:
                            tempSet.update(getEpsilonClosure(
                                NFA_Table, NewState))
                        if (mode == True):
                            DFA_Table[state][alph]=tempSet
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

    return DFA_Table,repr(startingNode)

def getDFA_Structure(DFA_Table, FinalNodes):
    #Creates the DFA structure
    DFAstructure = copy.deepcopy(DFA_Table)
    DFA_Final = set()
    for node in DFA_Table.keys():
        for input in DFA_Table[node].keys():
            if (DFAstructure[node][input] != {'Φ'}):
                DFAstructure[node][input] =  repr(DFA_Table[node][input])
            else:
                DFAstructure[node][input] = "Φ"
        if node != 'Φ':
            if FinalNodes.intersection(eval(node)):
                DFA_Final.add(node)
    return DFAstructure ,DFA_Final


def getEpsilonClosure(NFA_Table, nodeName):
    #Gets epsilon closure for the given Node
    EpsilonEquvNodes = set()
    EpsilonEquvNodes.update(NFA_Table[nodeName]["ε"])
    EpsilonEquvNodes.add(nodeName)
    EpsilonEquvNodes.discard("Φ")
    return EpsilonEquvNodes

startProcessing(json.loads("""
{
  "startNode":0,
  "nodes":[
    {
      "name":0,
      "typeOf":"FINAL",
      "edgeIndices":[0]
    },
    {
      "name":1,
      "typeOf":"FINAL",
      "edgeIndices":[0]
    }
  ],
  "edges":[
    {
      "fromNode":0,
      "toNode":1,
      "input":"a"
    }
  ],
  "alphabet":["a", "b", "c", "ε"],
  "mode":0
}
"""))
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
# garboNode4 = Node(5, "FINAL", [5, 6])
# nodes = [startingNode, garboNode1, garboNode2, garboNode3, garboNode4]

# edge0 = Edge(1, 2, "ε")
# edge1 = Edge(1, 3, "a")
# edge2 = Edge(2, 5, "a")
# edge3 = Edge(2, 4, "a")
# edge4 = Edge(3, 4, "b")
# edge5 = Edge(5, 4, "a")
# edge6 = Edge(5, 4, "b")
# edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6]

# answer = Convert2DFA(nodes, edges, Alphapet,0 , False)
# print("\nThe NFA TABLE is \n",answer[0], "\nThe DFA Structure is \n",answer[1])

# example2
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1, 2])
# garboNode4 = Node(2, "FINAL", [3, 4, 5])
# nodes = [startingNode, garboNode4]

# edge0 = Edge(1, 2, "a")
# edge1 = Edge(1, 1, "a")
# edge2 = Edge(1, 1, "b")
# edge3 = Edge(2, 2, "a")
# edge4 = Edge(2, 2, "b")
# edge5 = Edge(2, 1, "b")
# edges = [edge0, edge1, edge2, edge3, edge4, edge5]

# answer = Convert2DFA(nodes, edges, Alphapet,0 , False)
# print("\nThe NFA TABLE is \n",answer[0], "\nThe DFA Structure is \n",answer[1])


# example3
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1, 2])
# garboNode1 = Node(2, "NORMAL", [3])
# garboNode2 = Node(3, "FINAL", [])
# nodes = [startingNode, garboNode1, garboNode2]

# edge0 = Edge(1, 1, "a")
# edge1 = Edge(1, 1, "b")
# edge2 = Edge(1, 2, "a")
# edge3 = Edge(2, 3, "b")
# edges = [edge0, edge1, edge2, edge3]

# answer = Convert2DFA(nodes, edges, Alphapet,0 , True)
# print("\nThe NFA TABLE is \n",answer[0], "\nThe DFA Structure is \n",answer[1])


# example4
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0])
# garboNode1 = Node(2, "NORMAL", [1, 2])
# garboNode2 = Node(3, "FINAL", [3, 4, 5])
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

# answer = Convert2DFA(nodes, edges, Alphapet,0 , False)
# print("\nThe NFA TABLE is \n",answer[0], "\nThe DFA Structure is \n",answer[1])


# example5
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0])
# garboNode1 = Node(2, "FINAL", [1, 2, 3])
# garboNode2 = Node(3, "GOAL", [4])
# garboNode3 = Node(4, "GOAL", [5, 6])
# nodes = [startingNode, garboNode1, garboNode2, garboNode3]

# edge0 = Edge(1, 2, "ε")
# edge1 = Edge(2, 1, "b")
# edge2 = Edge(2, 2, "a")
# edge3 = Edge(2, 3, "a")
# edge4 = Edge(3, 4, "b")
# edge5 = Edge(4, 1, "a")
# edge6 = Edge(4, 4, "a")

# edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6]

# answer = Convert2DFA(nodes, edges, Alphapet,0 , True)
# print("\nThe NFA TABLE is \n",answer[0], "\nThe DFA Structure is \n",answer[1])


# example6
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1])
# garboNode1 = Node(2, "FINAL", [2, 3])
# garboNode2 = Node(3, "NORMAL", [4])
# garboNode3 = Node(4, "FINAL", [5, 6])
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

# answer = Convert2DFA(nodes, edges, Alphapet,0 , True)
# print("\nThe NFA TABLE is \n",answer[0], "\nThe DFA Structure is \n",answer[1])


# example7
# Alphapet = ["a", "b", "ε"]
# startingNode = Node(1, "START", [0, 1, 2])
# garboNode1 = Node(2, "NORMAL", [3, 4, 5])
# garboNode2 = Node(3, "FINAL", [6, 7, 8, 9])
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

# answer = Convert2DFA(nodes, edges, Alphapet,0 , False)
# print("\nThe NFA TABLE is \n",answer[0], "\nThe DFA Structure is \n",answer[1])

