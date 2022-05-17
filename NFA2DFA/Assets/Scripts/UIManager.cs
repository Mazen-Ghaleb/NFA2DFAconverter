using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Text;
using System;
using System.IO;
using System.Web;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;

public class UIManager : MonoBehaviour
{
    const string charSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    [DllImport("__Internal")]
    private static extern void fromUnityDisplayDFA(string str);

    [Serializable]
    public enum SearchAlgorithm
    {
        BFS = 0,
        DFS,
        UCS,
        DEPTH_LIMITED,
        ITERATIVE_DEEPENING,
        GREEDY,
        A_STAR
    }

    public static UIManager singleton = null;

    public Edge lastCreatedEdge { get; private set; }

    public Node selectedStartNode {
        get {
            return startNodeDropdown.options.Count > 0 ? nodes[startNodeDropdown.value] : null;
        }
    }

    public SearchAlgorithm selectedSearchAlgorithm {
        get {
            return (SearchAlgorithm)searchAlgorithmDropdown.value;
        }
    }

    public int maxDepth {
        get {
            return int.Parse(maxDepthInputField.text);
        }
    }

    public bool deleteFlag
    {
        get {
            foreach(KeyCode key in deleteKeys)
                if(Input.GetKey(key))
                    return true;
            
            return false;
        }
    }

    public string[] alphabet {
        get {
            return alphabetInputField.text.Split(',');
        }
    }

    public bool mode {
        get {
            return modeToggle.isOn;
        }
    }

    [Serializable]
    public struct PythonScript
    {
        // [SerializeField] public SearchAlgorithm algorithm;
        [SerializeField] public TextAsset ELF;
        [SerializeField] public TextAsset EXE;
    }

    [SerializeField] private Color activeNodeColor = Color.blue;
    [SerializeField] private Color pathNodeColor = Color.green;
    [SerializeField] private Transform visualizeUI;
    [SerializeField] private Text searchFailedText;
    [SerializeField] private Text searchSucceededText;
    [SerializeField] private Node nodePrefab;
    [SerializeField] private Edge edgePrefab;
    [SerializeField] private Transform nodeList;
    [SerializeField] private Transform edgeList;
    [SerializeField] private Dropdown startNodeDropdown;
    [SerializeField] private Dropdown searchAlgorithmDropdown;
    [SerializeField] private InputField maxDepthInputField;
    [SerializeField] private InputField alphabetInputField;
    [SerializeField] private Toggle modeToggle;
    [SerializeField] private Button runSearchButton;
    [SerializeField] private Button addNodeButton;
    [SerializeField] private KeyCode[] deleteKeys;
    [SerializeField] private PythonScript script;
    // [SerializeField] private PythonScript[] pythonScripts;

    private string defaultMaxDepth = null;
    private string NameCounter = "A";
    private List<Node> nodes = new List<Node>();
    private List<Edge> edges = new List<Edge>();
    private IEnumerator visualizationCoroutine = null;
    private JsonOutput lastOutput = null;

    private void Awake()
    {
        if(singleton != null)
        {
            Debug.LogWarning("Two UIManager scripts in the same scene...");
            gameObject.SetActive(false);
            return;
        }

        singleton = this;
        // Application.targetFrameRate = targetFrameRate;
    }

    private void Start()
    {
        defaultMaxDepth = maxDepthInputField.text;
        UpdateUI();
    }

    public void CreateNode()
    {
        Node prevSelectedStartNode = selectedStartNode;

        Node newNode = Instantiate(nodePrefab.gameObject, nodeList).GetComponent<Node>();
        nodes.Add(newNode);

        newNode.transform.position = new Vector2(Input.mousePosition.x, Input.mousePosition.y);
        newNode.BeginDrag();
        newNode.nodeName = GenerateName();

        UpdateUI();
        UpdateStartNodeDropdown(prevSelectedStartNode);
    }

    public void CreateEdge(Node sourceNode)
    {
        // Make sure you can only create one edge at a time
        if(lastCreatedEdge != null && !lastCreatedEdge.assigned) return;

        Edge newEdge = Instantiate(edgePrefab.gameObject, edgeList).GetComponent<Edge>();
        edges.Add(newEdge);
        lastCreatedEdge = newEdge;

        newEdge.AssignNode(sourceNode);
        SetEditingAllowed(false);
    }

    public void DeleteNode(Node node)
    {
        Node prevSelectedStartNode = selectedStartNode;

        for(int i = 0; i < edges.Count; i++)
        {
            Edge edge = edges[i];
            if(edge.fromNode == node || edge.toNode == node)
            {
                DeleteEdge(edge);
                i--;
            }
        }

        nodes.Remove(node);
        Destroy(node.gameObject);

        UpdateUI();
        UpdateStartNodeDropdown(prevSelectedStartNode);
    }
    
    public void DeleteEdge(Edge edge)
    {
        if(edge == lastCreatedEdge)
            lastCreatedEdge = null;

        edges.Remove(edge);
        Destroy(edge.gameObject);
    }

    public void RunSearch()
    {
        // PythonScript? chosenScript = null; 
        // foreach(PythonScript script in pythonScripts)
        //     if(script.algorithm == selectedSearchAlgorithm)
        //     {
        //         chosenScript = script;
        //         break;
        //     }
        
        // if(chosenScript == null)
        // {
        //     Debug.LogError("Script not added to the list of scripts");
        //     return;
        // }

        JsonInput input = GenerateJSON();//JsonUtility.ToJson(
        
// #if UNITY_EDITOR_WIN || UNITY_STANDALONE_WIN
//         // TextAsset program = chosenScript.Value.EXE;
//         TextAsset program = script.EXE;
//         string extension = "exe";
// #else
//         // TextAsset program = chosenScript.Value.ELF;
//         TextAsset program = script.ELF;
//         string extension = "elf";
// #endif
        // lastOutput = ExecutePythonScript(input); 
        ExecutePythonScript(input); 

        // RunVizualizationAsync();
    }

    public void RunVizualizationAsync()
    {
        StopVizualization();

        SetEditingAllowed(false);

        visualizationCoroutine = RunVisualization(lastOutput);
        StartCoroutine(visualizationCoroutine);
    }

    public void StopVizualization()
    {
        if(visualizationCoroutine != null)
            StopCoroutine(visualizationCoroutine);
        
        SetEditingAllowed(true);
        ResetNodeColors();
        
        visualizeUI.gameObject.SetActive(false);
    }

    public JsonInput GenerateJSON()
    {
        return new JsonInput(selectedSearchAlgorithm, maxDepth, selectedStartNode, nodes, edges);
    }

    public Edge GetEdge(Node fromNode, Node toNode)
    {
    	foreach(Edge edge in edges)
            if(edge.fromNode == fromNode && edge.toNode == toNode)
                return edge;
        
        return null;
    }

    public bool IsNameTaken(Node targetNode)
    {
    	foreach(Node node in nodes)
            if(node.nodeName == targetNode.nodeName && node != targetNode)
                return true;
        
        return false;
    }

    public void UpdateUI()
    {
        runSearchButton.interactable = nodes.Count > 0;

        maxDepthInputField.interactable = selectedSearchAlgorithm == SearchAlgorithm.DEPTH_LIMITED || selectedSearchAlgorithm == SearchAlgorithm.ITERATIVE_DEEPENING;
        if(maxDepthInputField.text.Length == 0)
            maxDepthInputField.text = defaultMaxDepth;

        UpdateStartNodeDropdown();
    }

    public void SetEditingAllowed(bool allowed)
    {
        foreach(Node node in nodes) node.interactable = allowed;
        foreach(Edge edge in edges) edge.interactable = allowed;

        startNodeDropdown.interactable = allowed;
        searchAlgorithmDropdown.interactable = allowed;
        maxDepthInputField.interactable = allowed;
        runSearchButton.interactable = allowed;
        addNodeButton.interactable = allowed;

        if(allowed) UpdateUI();
    }

    public void AlphabetValueChanged()
    {
        alphabetInputField.text = Regex.Replace(alphabetInputField.text, @"[^a-zA-Z0-9,]", "");
    }

    public void AlphabetUpdated()
    {
        AlphabetValueChanged();

        string[] symbols = alphabetInputField.text.Split(',').Distinct().ToArray();

        List<string> finalSymbols = new List<string>(symbols);
        finalSymbols.Remove("");
        finalSymbols.Add("");

        alphabetInputField.text = String.Join(",", finalSymbols);
    }

    private void ExecutePythonScript(JsonInput input)
    {
//         string path = Path.Combine(Path.GetTempPath(), Guid.NewGuid().ToString() + "." + extension);
//         string jsonPath = path + ".json";
//         print(path); // TODO
//         print(jsonPath); // TODO

//         File.WriteAllBytes(path, script.bytes);
// #if UNITY_EDITOR_LINUX || UNITY_STANDALONE_LINUX || UNITY_EDITOR_OSX || UNITY_STANDALONE_OSX
//         System.Diagnostics.Process.Start("chmod", "+x " + path).WaitForExit();
// #endif
        string jsonString = JsonUtility.ToJson(input);
        print(jsonString);
        // jsonString = HttpUtility.UrlEncode(jsonString);
        // print(jsonString);
        fromUnityDisplayDFA(jsonString);

        // File.WriteAllText(jsonPath, jsonString);

        // System.Diagnostics.ProcessStartInfo info = new System.Diagnostics.ProcessStartInfo(path);
        // info.Arguments = "\""+System.Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(jsonPath))+"\"";
        // print(info.Arguments); // TODO
        // using(System.Diagnostics.Process process = System.Diagnostics.Process.Start(info))
        //     process.WaitForExit();

        // File.Delete(path);
        // jsonString = File.ReadAllText(jsonPath);
        // print(jsonString);
        // File.Delete(jsonPath);

        // JsonOutput output = JsonUtility.FromJson<JsonOutput>(jsonString);
        // return output;
    }

    private IEnumerator RunVisualization(JsonOutput output) 
    {
        visualizeUI.gameObject.SetActive(true);
        searchFailedText.gameObject.SetActive(false);
        searchSucceededText.gameObject.SetActive(false);

        if(output.visitedEdges.Length != output.visitedNodes.Length - 1)
        {
            Debug.LogError("output.visitedEdges.Length must be equal to output.visitedNodes.Length - 1");
            yield break;
        }

        if(output.PathvisitedEdges != null && output.PathvisitedNodes != null && output.PathvisitedEdges.Length != output.PathvisitedNodes.Length - 1)
        {
            Debug.LogError("output.PathvisitedEdges.Length must be equal to output.PathvisitedNodes.Length - 1");
            yield break;
        }

        for(int i = 0; i < output.visitedNodes.Length; i++)
        {
            yield return new WaitForSeconds(0.5f);
            int nodeIndex = output.visitedNodes[i];
            if (nodeIndex == -1)
                ResetNodeColors();
            else
                nodes[nodeIndex].color = nodes[nodeIndex].isGoal ? pathNodeColor : activeNodeColor;

            if(i < output.visitedEdges.Length)
            {
                yield return new WaitForSeconds(1f);
                int edgeIndex = output.visitedEdges[i];
                if (edgeIndex == -1)
                    ResetNodeColors();
                else
                    edges[edgeIndex].color = activeNodeColor;
            }
        }

        if(!output.failed && output.PathvisitedEdges != null && output.PathvisitedNodes != null)
        {
            for(int i = 0; i < output.PathvisitedNodes.Length; i++)
            {
                nodes[output.PathvisitedNodes[i]].color = pathNodeColor;

                if(i < output.PathvisitedEdges.Length)
                    edges[output.PathvisitedEdges[i]].color = pathNodeColor;
            }
        }
        
        if(output.failed)
            searchFailedText.gameObject.SetActive(true);
        else
            searchSucceededText.gameObject.SetActive(true);

        visualizationCoroutine = null;
    }

    private string GenerateName()
    {
        StringBuilder newName = new StringBuilder(NameCounter);

        int carry = 0;
        for(int i = newName.Length - 1; i >= 0; i--)
        {
            int newCharIndex = charSet.IndexOf(newName[i])+carry;
            if(i == newName.Length - 1)
                newCharIndex += 1;
            else if (carry == 0)
                break;

            if(newCharIndex >= charSet.Length)
            {
                newName[i] = charSet[newCharIndex % charSet.Length];

                if(i == 0)
                {
                    i++;
                    newName.Insert(0, "A");
                    carry = 0;
                }
                else
                    carry = 1;
            }
            else
            {
                carry = 0;
                newName[i] = charSet[newCharIndex];
            }
        }

        string name = NameCounter;
        NameCounter = newName.ToString();

        return name;
    }

    private void UpdateStartNodeDropdown(Node prevSelected = null)
    {
        startNodeDropdown.options.Clear();

        for(int i = 0; i < nodes.Count; i++)
            startNodeDropdown.options.Add(new Dropdown.OptionData(nodes[i].nodeName));

        int index = prevSelected == null ? nodes.IndexOf(selectedStartNode) : nodes.IndexOf(prevSelected);
        startNodeDropdown.value = index == -1 ? 0 : index;
        startNodeDropdown.RefreshShownValue();
    }

    private void ResetNodeColors()
    {
        foreach(Node node in nodes) node.color = null;
        foreach(Edge edge in edges) edge.color = null;
    }
}
