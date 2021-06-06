# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import random
import socket
import time
from Models import IzhikevichNeuron, SingleExponentialSynapse
np.random.seed(seed=1234)


def simulation_1sec():
    voltages = np.zeros([num_neurons, nt])
    spikes = np.zeros([num_neurons, nt])
    currents = np.zeros([num_neurons, nt])

    for t in range(nt):
        I = synapses(np.dot(synaptic_weights, poisson_spikes[:, t])) * 1000

        for i in range(num_neurons):
            spikes[i, t] = output_neurons[i](I[i])
            voltages[i, t] = output_neurons[i].v_

        currents[:, t] = I

    return np.sum(spikes, axis=1), voltages, spikes, currents


dt = 1.0; T = 1000 # ms
nt = round(T/dt)
t = np.arange(nt) * dt

# 今は入力・出力同じ数で
num_neurons = 8


# fr_in = 30.0 # ポアソンスパイクの発火率 (Hz)
input_fr = np.random.uniform(low=15.0, high=45.0, size=num_neurons)
# poisson_spikes = np.where(np.random.rand(num_neurons, nt) < fr_in / nt, 1, 0)


output_neurons = []
# ニューロンの初期化（シナプス荷重はあとで掛ける
for i in range(num_neurons):
    C = 100 # random.randint(50, 150)
    a = 0.03 # random.uniform(0.01, 0.03)
    b = -2 # random.randint(-5, 5)
    k = 0.7 # random.uniform(0.5, 2.0)
    d = 100 # random.randint(100, 200)
    output_neurons.append(IzhikevichNeuron(dt=dt, C=C, a=a, b=b, k=k, d=d))

    output_neurons[i].initialize_states()


synapses = SingleExponentialSynapse(N=num_neurons, dt=dt, td=50.0)
synaptic_weights = np.random.normal(loc=2.0, scale=.0, size=num_neurons) # 対角行列の対角成分を生成(loc:平均,scale:標準偏差)
synaptic_weights = np.ones(num_neurons) * 3.0
synaptic_weights = np.diag(synaptic_weights) # 対角行列にする


"""
_, voltages, _, _ = simulation_1sec()

x = np.arange(nt)
for i in range(num_neurons):
    plt.subplot(num_neurons*2, 1, i*2+1)
    # plt.plot(x, voltages[i])
    plt.plot(x, poisson_spikes[i], 'ko', markersize=2)
    plt.ylim(0.9, 1.1)
    plt.subplot(num_neurons*2, 1, i*2+2)
    plt.plot(x, voltages[i])
    plt.ylim(-100, 100)
plt.show()
"""



HOST = '127.0.0.1'
PORT_SEND = 50001
PORT_RECEIVE = 50002

client_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_receive.bind((HOST, PORT_RECEIVE))


while True:

    cosines_byte, _ = client_receive.recvfrom(1024) # BufferSize
    cosines_str = cosines_byte.decode()
    cosines_strlist = cosines_str.split(',')
    cosines = np.zeros(num_neurons)
    for i in range(num_neurons):
        cosines[i] = float(cosines_strlist[i])
    input_fr = (cosines + 1) * 30
    print(f"Input frequencies: {input_fr}")

    # poisson_spikes = np.where(np.random.rand(num_neurons, nt) < fr_in / nt, 1, 0)
    poisson_spikes = np.zeros([num_neurons, nt])
    for i in range(num_neurons):
        poisson_spikes[i] = np.where(np.random.rand(nt) < input_fr[i] / nt, 1, 0)
        # print(np.sum(poisson_spikes[i]))


    freqs, _,_,_ = simulation_1sec()
    print(f"Output frequencies: {freqs}")


    client_send.sendto(str(freqs).encode('utf-8'), (HOST, PORT_SEND))

    time.sleep(1.0)
