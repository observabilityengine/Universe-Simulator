"""
Universe Simulator - Adan Optimizer
Original adaptive Nesterov momentum algorithm.
"""

from __future__ import annotations

import math
from typing import List

class Adan:
    def __init__(self, params: List[float], lr: float = 0.001, beta1: float = 0.98, beta2: float = 0.92, beta3: float = 0.99, eps: float = 1e-8):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.beta3 = beta3
        self.eps = eps
        self.m = [0.0] * len(params)
        self.v = [0.0] * len(params)
        self.n = [0.0] * len(params)
        self.prev_g = [0.0] * len(params)
        self.t = 0

    def step(self, grads: List[float]) -> None:
        self.t += 1
        for i, g in enumerate(grads):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (g - self.prev_g[i])
            self.n[i] = self.beta3 * self.n[i] + (1 - self.beta3) * (g + self.beta2 * (g - self.prev_g[i])) ** 2
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            n_hat = self.n[i] / (1 - self.beta3 ** self.t)
            self.params[i] -= self.lr * (m_hat + self.beta2 * v_hat) / (math.sqrt(n_hat) + self.eps)
            self.prev_g[i] = g

if __name__ == "__main__":
    opt = Adan([0.0], lr=0.1)
    for _ in range(100):
        x = opt.params[0]
        g = 2 * (x - 2.5)
        opt.step([g])
    assert abs(opt.params[0] - 2.5) < 0.4
    print("adan self-test passed", opt.params[0])
