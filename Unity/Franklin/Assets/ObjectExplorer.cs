using UnityEngine;

public class ObjectExplorer : MonoBehaviour
{
    public Transform target;             // Object to explore
    public float rotationSpeed = 3f;
    public float zoomSpeed = 5f;
    public float minZoom = 2f;
    public float maxZoom = 15f;
    public float panSpeed = 0.5f;

    private float distance;
    private Vector3 offset;
    private Vector3 lastMousePos;

    void Start()
    {
        if (target == null)
        {
            Debug.LogError("Target not assigned to ObjectExplorer script.");
            enabled = false;
            return;
        }

        distance = Vector3.Distance(transform.position, target.position);
        offset = (transform.position - target.position).normalized;
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0) || Input.GetMouseButtonDown(1))
            lastMousePos = Input.mousePosition;

        Vector3 mouseDelta = Input.mousePosition - lastMousePos;
        lastMousePos = Input.mousePosition;

        // Left click: rotate around object
        if (Input.GetMouseButton(0))
        {
            Quaternion rotX = Quaternion.AngleAxis(mouseDelta.x * rotationSpeed * Time.deltaTime, Vector3.up);
            Quaternion rotY = Quaternion.AngleAxis(-mouseDelta.y * rotationSpeed * Time.deltaTime, transform.right);
            offset = rotX * rotY * offset;
        }

        // Right click: pan
        if (Input.GetMouseButton(1))
        {
            Vector3 right = transform.right;
            Vector3 up = transform.up;
            Vector3 panOffset = (-right * mouseDelta.x + -up * mouseDelta.y) * panSpeed * Time.deltaTime;
            target.position += panOffset;
        }

        // Scroll wheel: zoom
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        distance -= scroll * zoomSpeed;
        distance = Mathf.Clamp(distance, minZoom, maxZoom);

        // Update camera position
        transform.position = target.position + offset * distance;
        transform.LookAt(target);
    }
}
