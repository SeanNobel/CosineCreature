using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetController : MonoBehaviour
{
    float move = 10f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(Input.GetKeyDown(KeyCode.LeftArrow)) {
            transform.Translate(-this.move, 0f, 0f);
        }else if(Input.GetKeyDown(KeyCode.RightArrow)) {
            transform.Translate(this.move, 0f, 0f);
        }else if(Input.GetKeyDown(KeyCode.UpArrow)) {
            transform.Translate(0f, 0f, this.move);
        }else if(Input.GetKeyDown(KeyCode.DownArrow)) {
            transform.Translate(0f, 0f, -this.move);
        }
    }
}
