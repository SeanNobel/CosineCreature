using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreatureController : MonoBehaviour
{
    int num_neurons = 8;
    float power = 100f;

    Rigidbody rb;
    Vector3[] baseVectors;

    Brain brainScript;

    private float[] firing_rates;

    // Start is called before the first frame update
    void Start()
    {
        this.rb = this.GetComponent<Rigidbody>();

        this.baseVectors = new Vector3[] {
            Vector3.right, Vector3.left, Vector3.forward, Vector3.back,
            (Vector3.right + Vector3.forward) / Mathf.Sqrt(2),
            (Vector3.right + Vector3.back) / Mathf.Sqrt(2),
            (Vector3.left + Vector3.forward) / Mathf.Sqrt(2),
            (Vector3.left + Vector3.back) / Mathf.Sqrt(2)
        };


        this.brainScript = GameObject.Find("Brain").GetComponent<Brain>();
    }

    // Update is called once per frame
    void Update()
    {
        this.firing_rates = brainScript.firing_rates;

        Vector3 force = Vector3.zero;
        for(int i=0; i<num_neurons; i++) {
            force += this.firing_rates[i] * this.baseVectors[i] / 10f;
        }

        this.rb.AddForce(force);

        Debug.Log(force[0]);
    }
}
