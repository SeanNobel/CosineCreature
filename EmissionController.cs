using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EmissionController : MonoBehaviour
{
    Brain brainScript;

    public int neuron_id = 0;

    Material mat;

    // Start is called before the first frame update
    void Start()
    {
        this.mat = gameObject.GetComponent<MeshRenderer>().material;

        this.brainScript = GameObject.Find("Brain").GetComponent<Brain>();
    }

    // Update is called once per frame
    void Update()
    {
        float intensity = Mathf.Pow(this.brainScript.firing_rates[this.neuron_id], 2.2f) * 0.0001f;
        // Debug.Log(intensity);
        this.mat.SetColor("_EmissionColor", new Color(1f*intensity, 6f*intensity, 3f*intensity));
        // this.mat.SetColor("_EmissionColor", new Color(0.01f, 0.6f, 0.3f));
    }
}
