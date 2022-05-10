using System;
using UnityEngine;
using UnityEngine.UI;

using System.Linq;
using System.Text.RegularExpressions;

// [RequireComponent(typeof(RectTransform))]
[Serializable]
public class Edge : MonoBehaviour
{
    enum EdgeState {
        NORMAL,
        REVERSED,
        TWO_WAY
    }

    public bool assigned {
        get { return fromNode != null && toNode != null; }
    }

    public bool isDirected {
        get { return state != EdgeState.TWO_WAY; }
    }

    public string trigger {
        get { return weightInputField.text; }
    }

    public bool interactable {
        get {
            return editable;
        }
        set {
            editable = value;
            weightInputField.interactable = value;
        }
    }

    public Color? color {
        get {
            return coloredImage.color;
        }
        set {
            coloredImage.color = value == null ? defaultColor : value.Value;
        }
    }
    
    public Node fromNode { get; private set; } = null;
    public Node toNode { get; private set; } = null;

    [SerializeField] private Image coloredImage;
    [SerializeField] private RectTransform lineRectTransform = null;
    [SerializeField] private RectTransform extraArrowhead = null;
    [SerializeField] private RectTransform loop = null;
    [SerializeField] private RectTransform loopInputFieldPivot = null;
    [SerializeField] private InputField weightInputField = null;
    [SerializeField] private float assignedLengthOffset = 0;
    [SerializeField] private float heightOffset = 0;
    [SerializeField] private float inputFieldOffset = 0;

    private bool editable = true;
    private string weightDefaultValue;
    private EdgeState state = EdgeState.NORMAL;
    private Color defaultColor;

    public void AssignNode(Node node)
    {
        if (fromNode == null)
            fromNode = node;
        else if (toNode == null)
        {
            UIManager.singleton.SetEditingAllowed(true);

            Edge existingEdge = UIManager.singleton.GetEdge(fromNode, node);
            if(existingEdge)
            {
                // existingEdge.weightInputField.text = existingEdge.weightInputField.text + ",";
                // existingEdge.weightInputField.text.position = existingEdge.weightInputField.text.Length - 1;
                existingEdge.weightInputField.Select();
                UIManager.singleton.DeleteEdge(this);
                return;
            }
            
            toNode = node;
            if(fromNode == toNode)
            {
                lineRectTransform.gameObject.SetActive(false);
                extraArrowhead.gameObject.SetActive(false);
                loop.gameObject.SetActive(true);
            }
        }
        else
            Debug.LogError("Cannot set edge node (edge already assigned)");
    }

    public void PointerClick()
    {
        if(!editable) return;
        UIManager.singleton.DeleteEdge(this);
        

        // if(UIManager.singleton.deleteFlag)
        // {
        //     UIManager.singleton.DeleteEdge(this);
        //     return;
        // }

        // state = (EdgeState)((int)(state+1) % Enum.GetNames(typeof(EdgeState)).Length);

        // extraArrowhead.gameObject.SetActive(state == EdgeState.TWO_WAY);
        // if(state != EdgeState.TWO_WAY)
        //     (fromNode, toNode) = (toNode, fromNode);
    }

    public void WeightValueChanged()
    {
        weightInputField.text = Regex.Replace(weightInputField.text, @"[^a-zA-Z0-9,]", "");
    }

    public void WeightUpdated()
    {
        WeightValueChanged();

        string[] symbols = weightInputField.text.Split(',');
        symbols = symbols.Distinct().ToArray();

        weightInputField.text = String.Join(",", symbols);

        // weightInputField.text = Regex.Replace(weightInputField.text, @"[^a-zA-Z0-9,]", "");
    }

    private void Start()
    {
        if(lineRectTransform == null)
            Debug.LogWarning("lineRectTransform not assigned and will never be assigned");
        weightDefaultValue = weightInputField.text;
        defaultColor = color.Value;
    }

    private void Update()
    {
        if(fromNode == toNode)
        {
            transform.position = fromNode.loopPosition; //.transform.position + Vector3.up * (fromNode.GetComponent<RectTransform>().rect.height / 2) + loopExtraOffset;
            transform.rotation = fromNode.loopRotation; 

            weightInputField.transform.position = loopInputFieldPivot.transform.position;
            weightInputField.transform.rotation = loopInputFieldPivot.transform.rotation;
        }
        else if(fromNode != null)
        {
            Vector2 sourcePos = fromNode.transform.position;
            Vector2 targetPos = !assigned ? Input.mousePosition : toNode.transform.position;
            
            lineRectTransform.sizeDelta = new Vector2(Vector2.Distance(sourcePos, targetPos) / ScrollviewZoom.singleton.currentScale, lineRectTransform.sizeDelta.y);
            if(assigned)
                lineRectTransform.sizeDelta += Vector2.right * assignedLengthOffset;

            transform.position = Vector2.Lerp(sourcePos, targetPos, 0.5f);
            transform.rotation = Quaternion.LookRotation((targetPos - sourcePos).normalized);

            if(toNode != null)
            {
                float offsetMultiplier = fromNode.transform.position.x < toNode.transform.position.x ? 1 : -1;
                offsetMultiplier *= ScrollviewZoom.singleton.currentScale;

                transform.position += transform.up * heightOffset * offsetMultiplier;
                weightInputField.transform.localPosition = new Vector3(weightInputField.transform.localPosition.x, inputFieldOffset * offsetMultiplier, weightInputField.transform.localPosition.z);
            }

            weightInputField.transform.rotation = Quaternion.identity;

            if(!assigned && Input.GetKey(KeyCode.Escape))
            {
                UIManager.singleton.DeleteEdge(this);
                UIManager.singleton.SetEditingAllowed(true);
            }
        }
    }
}
