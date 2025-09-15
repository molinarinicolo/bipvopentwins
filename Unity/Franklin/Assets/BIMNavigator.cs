using UnityEngine;
using static ColorChanger;

public class BIMNavigation : MonoBehaviour
{
    public Transform target; // Your BIM model or center point
    public float rotationSpeed = 3.0f;
    public float zoomSpeed = 5.0f;
    public float panSpeed = 0.5f;
    public float minDistance = 2f;
    public float maxDistance = 50f;

    private float currentDistance;
    private Vector3 offset;
    private Vector3 lastMousePosition;

    void Start()
    {
        if (target == null)
        {
            Debug.LogError("Target is not set on BIMNavigation.");
            return;
        }

        currentDistance = Vector3.Distance(transform.position, target.position);
        offset = (transform.position - target.position).normalized;

    }

    void Update()
    {

        // Start tracking mouse
        if (Input.GetMouseButtonDown(0) || Input.GetMouseButtonDown(1))
        {
            lastMousePosition = Input.mousePosition;
        }

        Vector3 mouseDelta = Input.mousePosition - lastMousePosition;
        lastMousePosition = Input.mousePosition;

        // Left-click and drag to rotate around the target
        if (Input.GetMouseButton(0))
        {
            float yaw = mouseDelta.x * rotationSpeed * Time.deltaTime;
            float pitch = -mouseDelta.y * rotationSpeed * Time.deltaTime;

            Quaternion rot = Quaternion.Euler(pitch, yaw, 0);
            offset = rot * offset;
        }

        // Right-click and drag to pan the camera
        if (Input.GetMouseButton(1))
        {
            Vector3 right = transform.right;
            Vector3 up = transform.up;
            Vector3 panMovement = (-mouseDelta.x * right + -mouseDelta.y * up) * panSpeed * Time.deltaTime;
            target.position += panMovement;
        }

        // Scroll to zoom
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        currentDistance -= scroll * zoomSpeed;
        currentDistance = Mathf.Clamp(currentDistance, minDistance, maxDistance);

        // Update camera position
        transform.position = target.position + offset * currentDistance;
        transform.LookAt(target);

    }
}