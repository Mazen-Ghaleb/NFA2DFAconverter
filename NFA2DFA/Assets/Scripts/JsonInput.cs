using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

[Serializable]
public class JsonInput
{
    [Serializable]
    public class JsonNode
    {
        public string typeOf;
        // public float heuristic;
        // public int depth;
        public int[] edgeIndices;
        
        public JsonNode(Node node, List<Edge> edges, bool isStartNode)
        {
            this.typeOf = node.isGoal ? "FINAL" : "NORMAL"; 
            // this.heuristic = node.heuristic;
            // this.depth = 0;

            List<int> edgeIndices = new List<int>();
            for(int i = 0; i < edges.Count; i++)
                if(edges[i].fromNode == node || (edges[i].toNode == node && !edges[i].isDirected))
                    edgeIndices.Add(i);
                    
            this.edgeIndices = edgeIndices.ToArray();
        }
    }

    [Serializable]
    public class JsonEdge
    {
        public int fromNode;
        public int toNode;
        // public bool isDirected;
        // public float weight;

        public JsonEdge(Edge edge, List<Node> nodes)
        {
            this.fromNode = nodes.IndexOf(edge.fromNode);
            this.toNode = nodes.IndexOf(edge.toNode);
            // this.isDirected = edge.isDirected;
            // this.weight = edge.weight;
        }
    }

    public string algorithm;
    public int startNode;
    public int maxDepth;
    public JsonNode[] nodes;
    public JsonEdge[] edges;

    public JsonInput(UIManager.SearchAlgorithm algorithm, int maxDepth, Node startNode, List<Node> nodes, List<Edge> edges)
    {
        this.algorithm = algorithm.ToString();
        this.maxDepth = maxDepth;
        this.startNode = nodes.IndexOf(startNode);

        this.nodes = new JsonNode[nodes.Count];
        for(int i = 0; i < nodes.Count; i++)
            this.nodes[i] = new JsonNode(nodes[i], edges, nodes[i] == startNode);

        this.edges = new JsonEdge[edges.Count];
        for(int i = 0; i < edges.Count; i++)
            this.edges[i] = new JsonEdge(edges[i], nodes);
    }
}