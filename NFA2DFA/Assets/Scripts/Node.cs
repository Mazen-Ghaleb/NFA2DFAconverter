using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Node : MonoBehaviour
{
    public string nodeName {
        get { return nameInputField.text; }
        set
        {
            nameInputField.text = value;
            name = value;
        }
    }

    public float heuristic {
        get { return float.Parse(heuristicInputField.text); }
        set
        {
            heuristicInputField.text = value.ToString();
        }
    }
    
    public bool interactable {
        get {
            return editable;
        }
        set {
            editable = value;
            nameInputField.interactable = value;
            heuristicInputField.interactable = value;
            goalToggle.interactable = value;
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
    
    public bool isGoal {
        get {
            return goalToggle.isOn;
        }
    }

    public Vector3 loopPosition {
        get {
            return loopPivot.position;
        }
    }

    public Quaternion loopRotation {
        get {
            return loopPivot.rotation;
        }
    }

    [SerializeField] private Image coloredImage;
    [SerializeField] private InputField nameInputField;
    [SerializeField] private InputField heuristicInputField;
    [SerializeField] private Toggle goalToggle;
    [SerializeField] private RectTransform loopPivot;

    private bool editable = true;
    private bool isDragging = false;
    private Vector2 draggingOffset = Vector2.zero;
    private Color defaultColor;
    private float defaultheuristic;

    private void Start()
    {
        defaultColor = color.Value;
        defaultheuristic = heuristic;
    }

    private void Update()
    {
        if(isDragging)
            transform.position = new Vector2(Input.mousePosition.x, Input.mousePosition.y) + draggingOffset;
    }

    public void BeginDrag()
    {
        if(!editable) return;

        isDragging = true;
        nameInputField.enabled = false;
        heuristicInputField.enabled = false;
        goalToggle.enabled = false;
        draggingOffset = transform.position - Input.mousePosition;
        transform.SetAsLastSibling();
    }
    
    public void EndDrag()
    {
        isDragging = false;
        nameInputField.enabled = true;
        heuristicInputField.enabled = true;
        goalToggle.enabled = true;
    }

    public void PointerClick()
    {
        if(isDragging)
            EndDrag();
        else if (UIManager.singleton.lastCreatedEdge != null && !UIManager.singleton.lastCreatedEdge.assigned)
            UIManager.singleton.lastCreatedEdge.AssignNode(this);
        else if(editable)
        {
            if(UIManager.singleton.deleteFlag)
                UIManager.singleton.DeleteNode(this);
            else
                UIManager.singleton.CreateEdge(this);
        }
    }

    public void HeuristicChanged()
    {
        if(heuristicInputField.text.Length == 0)
            heuristicInputField.text = defaultheuristic.ToString();
    }

    public void NameChanged()
    {
        string originalName = nodeName;
        int counter = 0;
        while(UIManager.singleton.IsNameTaken(this))
            nodeName = originalName + ++counter;

        UIManager.singleton.UpdateUI();
    }
}
