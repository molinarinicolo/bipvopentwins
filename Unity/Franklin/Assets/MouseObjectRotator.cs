using UnityEngine;

public class MouseObjectRotator : MonoBehaviour
{
    private bool isDragging = false;
    private Vector3 lastMousePosition;
    public float rotationSpeed = 5f;

    void Update()
    {
        // Detect mouse down over the object
        if (Input.GetMouseButton(0))
        {
            RaycastHit hit;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

            // Check if we clicked this object
            if (Physics.Raycast(ray, out hit))
            {
                if (hit.transform == transform)
                {
                    isDragging = true;
                    lastMousePosition = Input.mousePosition;
                }
            }
        }

        // Stop dragging when the mouse is released
        if (Input.GetMouseButton(0))
        {
            isDragging = false;
        }

        // Rotate while dragging
        if (isDragging)
        {
            Vector3 delta = Input.mousePosition - lastMousePosition;
            float rotX = delta.y * rotationSpeed * Time.deltaTime;
            float rotY = -delta.x * rotationSpeed * Time.deltaTime;

            transform.Rotate(Camera.main.transform.up, rotY, Space.World);
            transform.Rotate(Camera.main.transform.right, rotX, Space.World);

            lastMousePosition = Input.mousePosition;
        }
    }
}
