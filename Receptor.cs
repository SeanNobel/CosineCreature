using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class Receptor : MonoBehaviour
{
    GameObject target;

    Vector3 direction;

    int num_neurons = 8;
    float[] cosines;

    string HOST = "127.0.0.1";
    int LOCA_LPORT = 50002;
    static UdpClient udp;
    float delta = 0f;

    Rigidbody rb;
    // Start is called before the first frame update
    void Start()
    {
        udp = new UdpClient();
        udp.Connect(HOST, LOCA_LPORT);

        this.target = GameObject.Find("Target");

        this.rb = this.GetComponent<Rigidbody>();

        // Initialize receptor neurons
        this.cosines = new float[this.num_neurons];
        for(int i=0; i<this.num_neurons; i++) {
            this.cosines[i] = 0f;
        }
    }

    // Update is called once per frame
    void Update()
    {
        this.direction = this.target.transform.position - this.transform.position;
        this.direction.Normalize();
        // Debug.Log(this.direction.ToString("F3")); // 勝手に少数第1位で切り上げされるので桁数を指定

        double tan_x = this.direction.z / this.direction.x;
        double rad = Math.Atan(tan_x);

        for(int i=0; i<this.num_neurons; i++) {
            this.cosines[i] = (float)Math.Cos(rad + 2d * Mathf.PI * i / this.num_neurons);
        }

        // Debug.Log(string.Join(", ", this.cosines));
    }

    void FixedUpdate() // Fixed Timestep: 0.02(s)
    {
        this.delta += Time.deltaTime;

        if(this.delta > 1f) {
            this.delta = 0f;

            string text = "";

            for(int i=0; i<this.num_neurons; i++) {
                text += this.cosines[i].ToString();
                if(i<this.num_neurons-1) text += ",";
            }

            byte[] data = Encoding.UTF8.GetBytes(text);
            udp.Send(data, data.Length);
        }
    }

    void OnApplicationQuit()
    {
        udp.Close();
    }
}
