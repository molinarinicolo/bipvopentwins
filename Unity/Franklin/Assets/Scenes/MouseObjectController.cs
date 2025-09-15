using UnityEngine;

public class MouseObjectController : MonoBehaviour
{
    public float rotationSpeed = 5.0f;
    public float zoomSpeed = 2.0f;
    public float panSpeed = 0.5f;

    private Vector3 lastMousePosition;

    void Update()
    {
        // Rotate with left mouse drag
        if (Input.GetMouseButton(0))
        {
            Vector3 delta = Input.mousePosition - lastMousePosition;
            float rotX = -delta.y * rotationSpeed * Time.deltaTime;
            float rotY = delta.x * rotationSpeed * Time.deltaTime;
            transform.Rotate(rotX, rotY, 0, Space.World);
        }

        // Zoom with scroll wheel
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        transform.position += transform.forward * scroll * zoomSpeed;

        // Pan with right mouse drag
        if (Input.GetMouseButton(1))
        {
            Vector3 delta = Input.mousePosition - lastMousePosition;
            Vector3 pan = new Vector3(-delta.x, -delta.y, 0) * panSpeed * Time.deltaTime;
            transform.Translate(pan, Space.Self);
        }

        lastMousePosition = Input.mousePosition;
    }
}