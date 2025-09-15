using UnityEngine;

public class MyData
{
    public string _time;
    public int _value;
    public bool description;
}

public class ColorChanger : MonoBehaviour
{
    // Call this function with a value between 0 and 5
    public void SetColorBasedOnValue(string values)
    {
        MyData data = JsonUtility.FromJson<MyData>(values);

        float val = data._value;
        // Clamp the value to be between 0 and 5
        Debug.Log(val);
        float value_clamped = Mathf.Clamp(val, 0f, 5f);

        // Normalize value to 0-1 range
        float t = value_clamped / 5f;

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
