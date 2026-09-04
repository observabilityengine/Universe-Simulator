"""
Universe Simulator - RAdam (Rectified Adam)
Original simplified implementation.
"""

from __future__ import annotations

import math
from typing import List

class RAdam:
    def __init__(self, params: List[float], lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [0.0] * len(params)
        self.v = [0.0] * len(params)
        self.t = 0
        self.rho_inf = 2 / (1 - beta2) - 1

    def step(self, grads: List[float]) -> None:
        self.t += 1
        for i, g in enumerate(grads):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g * g
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            rho_t = self.rho_inf - 2 * self.t * self.beta2 ** self.t / (1 - self.beta2 ** self.t)
            if rho_t > 4:
                v_hat = math.sqrt(self.v[i] / (1 - self.beta2 ** self.t))
                r_t = math.sqrt(((rho_t - 4) * (rho_t - 2) * self.rho_inf) / ((self.rho_inf - 4) * (self.rho_inf - 2) * rho_t))
                self.params[i] -= self.lr * r_t * m_hat / (v_hat + self.eps)
            else:
                self.params[i] -= self.lr * m_hat

if __name__ == "__main__":
    opt = RAdam([0.0], lr=0.1)
    for _ in range(150):
        x = opt.params[0]
        g = 2 * (x - 3)
        opt.step([g])
    assert abs(opt.params[0] - 3.0) < 0.25
    print("radam self-test passed", opt.params[0])
