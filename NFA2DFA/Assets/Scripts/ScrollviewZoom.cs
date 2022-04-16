using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScrollviewZoom : MonoBehaviour
{
    public static ScrollviewZoom singleton = null;
    public float currentScale { get; private set; } = 1;
    
    [SerializeField] private RectTransform content = null;
    [SerializeField] private float scaleMin = 0.25f;
    [SerializeField] private float scaleSpeed = 1;

    private void Awake()
    {
        if(singleton != null)
        {
            Debug.LogWarning("Two UIManager scripts in the same scene...");
            gameObject.SetActive(false);
            return;
        }

        singleton = this;
        if(content == null)
            Debug.LogWarning("Zoom content not assigned and will never be assigned");
    }

    private void Update()
    {
        float increment = Input.GetAxis("Mouse ScrollWheel");
        currentScale += increment * scaleSpeed;

        currentScale = Mathf.Clamp(currentScale, scaleMin, 1);

        if(content != null)
            content.localScale = Vector2.one * currentScale;
    }
}