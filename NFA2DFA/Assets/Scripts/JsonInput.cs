using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Linq;

[Serializable]
public class JsonInput
{
    [Serializable]
    public class JsonNode
    {
        public string name;
        public string typeOf;
        // public float heuristic;
        // public int depth;
        public int[] edgeIndices;
        
        public JsonNode(string node, bool isGoal,  JsonEdge[] edges, bool isStartNode)
        {
            this.name = node;
            this.typeOf = isGoal ? "FINAL" : "NORMAL"; 
            // this.heuristic = node.heuristic;
            // this.depth = 0;

            List<int> edgeIndices = new List<int>();
            for(int i = 0; i < edges.Count(); i++)
                if(edges[i].fromNode == node)
                    edgeIndices.Add(i);
                    
            this.edgeIndices = edgeIndices.ToArray();
        }
    }

    [Serializable]
    public class JsonEdge
    {
        public string fromNode;
        public string toNode;
        // public int fromNode;
        // public int toNode;
        public string input;
        // public bool isDirected;
        // public float weight;

        public JsonEdge(Edge edge, string trigger)
        {
            // this.fromNode = nodes.IndexOf(edge.fromNode);
            // this.toNode = nodes.IndexOf(edge.toNode);
            this.fromNode = edge.fromNode.nodeName;
            this.toNode = edge.toNode.nodeName;
            this.input = trigger;
            // this.isDirected = edge.isDirected;
            // this.weight = edge.weight;
        }
    }

    // public string algorithm;
    public int startNode;
    // public int maxDepth;
    public JsonNode[] nodes;
    public JsonEdge[] edges;
    public string[] alphabet;
    public int mode;

    public JsonInput(UIManager.SearchAlgorithm algorithm, int maxDepth, Node startNode, List<Node> nodes, List<Edge> edges)
    {
        List<JsonEdge> newEdges = new List<JsonEdge>();
        for(int i = 0; i < edges.Count(); i++)
        {
            string[] triggers = edges[i].trigger.Split(',').Distinct().ToArray();

            for(int j = 0; j < triggers.Length; j++)
                newEdges.Add(new JsonEdge(edges[i], triggers[j]));
        }
        this.edges = newEdges.ToArray();

        // this.algorithm = algorithm.ToString();
        // this.maxDepth = maxDepth;
        this.startNode = nodes.IndexOf(startNode);

        this.nodes = new JsonNode[nodes.Count];
        for(int i = 0; i < nodes.Count; i++)
            this.nodes[i] = new JsonNode(nodes[i].nodeName, nodes[i].isGoal, this.edges, nodes[i] == startNode);

        // this.edges = new JsonEdge[edges.Count];
        // for(int i = 0; i < edges.Count; i++)
        //     this.edges[i] = new JsonEdge(edges[i], nodes);

        List<string> alphabet = new List<string>();
        for(int i = 0; i < this.edges.Count(); i++)
            alphabet.Add(this.edges[i].input);

        alphabet.Add("");
        this.alphabet = alphabet.Distinct().ToArray();

        this.mode = 0;
    }
}