using UnityEngine;
using System.Collections.Generic;
using static VoltageColorChanger;

[System.Serializable]
public class GrafanaVoltageElement
{
    public string thingId;
    public float _value;
}

[System.Serializable]
public class GrafanaVoltage
{
    public GrafanaVoltageArray undefined;
}

[System.Serializable]
public class GrafanaVoltageArray
{
    public GrafanaVoltageElement[] undefined;
}

[System.Serializable]
public class GrafanaSeries
{
    public GrafanaVoltage series;
}

public class ColorVoltage : MonoBehaviour
{
    public static Dictionary<string, string> MPPTtoBIM = new Dictionary<string, string>();

    public void SetColorVoltage(string values)
    {
        Debug.Log("Entrato");
        MPPTtoBIM.Add("MPPT246", "Lama_doppia_Lama_doppia_[1609989]");
        MPPTtoBIM.Add("MPPT286", "Lama_L1L2_A_Lama_L1L2_A_[1612098]");
        MPPTtoBIM.Add("MPPT287", "Lama_L1L2_B_Lama_L1L2_B_[1613456]");

        GrafanaSeries series = JsonUtility.FromJson<GrafanaSeries>(values);
        GrafanaVoltage data = series.series;
        GrafanaVoltageArray dataArray = data.undefined;
        GrafanaVoltageElement[] dataArrayEl = dataArray.undefined;
        foreach (GrafanaVoltageElement d in dataArrayEl)
        {
            float val = d._value;
            string thing = d.thingId;
            string BIMId = MPPTtoBIM[thing];
            GameObject obj = GameObject.Find(BIMId);
            VoltageColorChanger colorChanger = obj.GetComponent<VoltageColorChanger>();
            colorChanger.SetColor(val);
        }
    }
}