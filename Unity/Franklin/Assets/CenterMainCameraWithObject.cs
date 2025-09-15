using UnityEngine;

public class CenterMainCameraWithObject : MonoBehaviour
{
    public Transform targetObject;
    public float padding = 1.5f;

    void Start()
    {
        if (targetObject == null)
        {
            Debug.LogWarning("No target object assigned.");
            return;
        }

        Camera cam = Camera.main;
        if (cam == null)
        {
            Debug.LogError("No Main Camera found in the scene.");
            return;
        }

        // Calculate object bounds
        Bounds bounds = CalculateBounds(targetObject);
        Vector3 center = bounds.center;
        float maxSize = Mathf.Max(bounds.size.x, bounds.size.y, bounds.size.z);

        // Calculate distance to frame object
        float distance = (maxSize * padding) / Mathf.Tan(Mathf.Deg2Rad * cam.fieldOfView * 0.5f);

        // Move camera
        Vector3 direction = cam.transform.forward * -1; // Reverse camera forward direction
        cam.transform.position = center + direction * distance;

        // Look at center
        cam.transform.LookAt(center);
    }

    Bounds CalculateBounds(Transform target)
    {
        Renderer[] renderers = target.GetComponentsInChildren<Renderer>();
        if (renderers.Length == 0)
            return new Bounds(target.position, Vector3.zero);

        Bounds bounds = renderers[0].bounds;
        foreach (Renderer r in renderers)
            bounds.Encapsulate(r.bounds);

        return bounds;
    }
}
