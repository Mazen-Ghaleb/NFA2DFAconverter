using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

[Serializable]
public class JsonOutput
{
    public int[] visitedNodes;
    public int[] visitedEdges;
    public bool failed;
    public int[] PathvisitedNodes;
    public int[] PathvisitedEdges;

    public JsonOutput(int[] visitedNodes, int[] visitedEdges, bool failed, int[] PathvisitedNodes, int[] PathvisitedEdges)
    {
        this.visitedNodes = visitedNodes;
        this.visitedEdges = visitedEdges;
        this.failed = failed;
        this.PathvisitedNodes = PathvisitedNodes;
        this.PathvisitedEdges = PathvisitedEdges;
    }
}
