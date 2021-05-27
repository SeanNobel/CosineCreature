using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Linq;

public class Brain : MonoBehaviour
{
    int LOCA_LPORT = 50001;
    static UdpClient udp;
    Thread thread;

    int num_neurons = 8;
    public float[] firing_rates;

    // Start is called before the first frame update
    void Start()
    {

        udp = new UdpClient(LOCA_LPORT);
        udp.Client.ReceiveTimeout = 2000;
        thread = new Thread(new ThreadStart(ThreadMethod));
        thread.Start();

        // Initialization
        this.firing_rates = new float[this.num_neurons];
        for(int i=0; i<this.num_neurons; i++) {
            this.firing_rates[i] = 0f;
        }
    }

    private void ThreadMethod()
    {
        while(true)
        {
            IPEndPoint remoteEP = null;
            byte[] data = udp.Receive(ref remoteEP);
            string text = Encoding.UTF8.GetString(data);

            if(remoteEP != null)
            {
                text = text.Remove(text.Length - 1);
                text = text.Remove(0, 1);

                // 一桁の値が来るとスペースで二回分割されて配列が長くなってしまうので
                List<string> fRate_strlist = new List<string>();
                fRate_strlist.AddRange(text.Split(' '));
                fRate_strlist.RemoveAll(s => s == "");
                string[] fRate_str = fRate_strlist.ToArray();
                Debug.Log(fRate_str.Length);

                for(int i=0; i<this.num_neurons; i++)
                {
                    this.firing_rates[i] = float.Parse(fRate_str[i]);
                }
            }
        }
    }

    void OnApplicationQuit()
    {
        thread.Abort();
    }
}
