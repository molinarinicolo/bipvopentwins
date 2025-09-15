using UnityEngine;

public class VoltageColorChanger : MonoBehaviour
{
    public void SetColor(float val)
    {
        
        float value_clamped = Mathf.Clamp(val, 0f, 15f);

        float t = value_clamped / 15f;
        // Interpolate from red to green
        Color newColor = Color.Lerp(Color.red, Color.green, t);

        // Apply the color to the object's material
        MeshRenderer renderer = GetComponent<MeshRenderer>();
        renderer.enabled = true;
        if (renderer != null)
        {
            Material uniqueMaterial = new Material(renderer.sharedMaterial);
            uniqueMaterial.SetColor("_BaseColor", newColor);
            renderer.material = uniqueMaterial;
            // Force update
            renderer.material = null;
            renderer.material = uniqueMaterial;
        }
        else
        {
            Debug.LogWarning("No Renderer found on this GameObject.");
        }
    }
}
