"""
Universe Simulator - Ranger Optimizer (RAdam + Lookahead)
Original combined implementation.
"""

from __future__ import annotations

import math
from typing import List

class Ranger:
    def __init__(self, params: List[float], lr: float = 0.001, alpha: float = 0.5, k: int = 5,
                 beta1: float = 0.95, beta2: float = 0.999, eps: float = 1e-5):
        self.params = list(params)
        self.slow = list(params)
        self.lr = lr
        self.alpha = alpha
        self.k = k
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [0.0] * len(params)
        self.v = [0.0] * len(params)
        self.t = 0
        self.step_count = 0
        self.rho_inf = 2 / (1 - beta2) - 1

    def step(self, grads: List[float]) -> None:
        self.t += 1
        self.step_count += 1
        for i, g in enumerate(grads):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g * g
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            rho_t = self.rho_inf - 2 * self.t * self.beta2 ** self.t / (1 - self.beta2 ** self.t)
            if rho_t > 4:
                v_hat = math.sqrt(self.v[i] / (1 - self.beta2 ** self.t))
                r = math.sqrt(((rho_t - 4) * (rho_t - 2) * self.rho_inf) / ((self.rho_inf - 4) * (self.rho_inf - 2) * rho_t))
                self.params[i] -= self.lr * r * m_hat / (v_hat + self.eps)
            else:
                self.params[i] -= self.lr * m_hat
        if self.step_count % self.k == 0:
            for i in range(len(self.params)):
                self.slow[i] += self.alpha * (self.params[i] - self.slow[i])
                self.params[i] = self.slow[i]

if __name__ == "__main__":
    opt = Ranger([0.0], lr=0.1)
    for _ in range(150):
        x = opt.params[0]
        g = 2 * (x - 2.5)
        opt.step([g])
    assert abs(opt.params[0] - 2.5) < 0.4
    print("ranger self-test passed", opt.params[0])
