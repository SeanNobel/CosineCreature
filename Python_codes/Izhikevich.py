# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import random
import socket
import time
from Models import IzhikevichNeuron, SingleExponentialSynapse


def simulation_1sec(): # 1秒間での各ニューロンの発火回数を返す
    I_base = np.random.randint(200, 400, num_neurons)
    I = np.full(num_neurons, I_base)
    # print(I)

    voltages = np.zeros([num_neurons, nt])
    spikes = np.zeros([num_neurons, nt])
    currents = np.zeros([num_neurons, nt])

    for t in range(nt):
        for i in range(num_neurons):
            spikes[i, t] = neurons[i](I[i])
            voltages[i, t] = neurons[i].v_

        currents[:, t] = synapses(spikes[:, t]) * 1000
        I = I_base + currents[:, t]
    # print(I)
    # print(currents.shape)

    return np.sum(spikes, axis=1), spikes, voltages, currents



dt = 1.0; T = 1000 # ms
nt = round(T/dt)
t = np.arange(nt) * dt

num_neurons = 8

neurons = []

for i in range(num_neurons): # ニューロンの初期化（シナプス荷重はあとで掛ける
    C = random.randint(50, 150)
    a = random.uniform(0.01, 0.03)
    b = random.randint(-5, 5)
    k = random.uniform(0.5, 2.0)
    d = random.randint(100, 200)
    neurons.append(IzhikevichNeuron(dt=dt, C=C, a=a, b=b, k=k, d=d))

    neurons[i].initialize_states()


synapses = SingleExponentialSynapse(N=num_neurons, dt=dt, td=50.0)
synaptic_weights = np.random.rand(num_neurons, num_neurons)

"""
_, _, _, currents = simulation_1sec()

x = np.arange(nt)
plt.plot(x, currents[0])
plt.show()
"""


HOST = '127.0.0.1'
PORT = 50001

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    freqs, _,_,_ = simulation_1sec()
    print(freqs)

    client.sendto(str(freqs).encode('utf-8'), (HOST, PORT))

    time.sleep(1.0)
