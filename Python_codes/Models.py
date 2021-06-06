# -*- coding: utf-8 -*-
# Basically using https://github.com/takyamamoto/SNN-from-scratch-with-Python
import numpy as np

class IzhikevichNeuron: # 1クラス1ニューロン
    def __init__(self, dt=1.0, C=100, a=0.02, b=0,
                    k=2.0, d=200, vrest=-60, vreset=-40, vthr=-40, vpeak=35):
        self.dt = dt
        self.C = C
        self.a = a; self.b = b; self.k = k; self.d = d
        self.vrest = vrest; self.vreset = vreset; self.vthr = vthr; self.vpeak = vpeak

        self.u = 0
        self.v = self.vrest
        self.v_ = self.v

    def initialize_states(self, random_state=False):
        if random_state:
            self.v = self.vreset + np.random.rand() * (self.vthr - self.vreset)
        else:
            self.v = self.vrest
        self.u = 0

    def __call__(self, I):
        dv = (self.k * (self.v - self.vrest) * (self.v - self.vthr) - self.u + I) / self.C
        v = self.v + self.dt * dv
        u = self.u + self.dt * (self.a * (self.b * (self.v_ - self.vrest) - self.u))

        s = 1 * (v>=self.vpeak) #発火時は1, その他は0の出力

        self.u = u + self.d * s
        self.v = v * (1-s) + self.vreset * s
        self.v_ = self.v

        return s


class SingleExponentialSynapse:
    def __init__(self, N, dt=1.0, td=50.0):
        self.N = N
        self.dt = dt
        self.td = td
        self.r = np.zeros(N)

    def initialize_states(self):
        self.r = np.zeros(self.N)

    def __call__(self, spike): # spike: 0 or 1
        r = self.r * (1 - self.dt / self.td) + spike / self.td
        self.r = r # 内的状態
        return r
