"""
Universe Simulator - LAMB Optimizer (Layer-wise Adaptive Moments)
Original simplified implementation.
"""

from __future__ import annotations

import math
from typing import List

class LAMB:
    def __init__(self, params: List[float], lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-6):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [0.0] * len(params)
        self.v = [0.0] * len(params)
        self.t = 0

    def step(self, grads: List[float]) -> None:
        self.t += 1
        for i, g in enumerate(grads):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g * g
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            update = m_hat / (math.sqrt(v_hat) + self.eps)
            w_norm = abs(self.params[i]) + self.eps
            u_norm = abs(update) + self.eps
            trust = w_norm / u_norm
            self.params[i] -= self.lr * trust * update

if __name__ == "__main__":
    opt = LAMB([0.0], lr=0.1)
    for _ in range(100):
        x = opt.params[0]
        g = 2 * (x - 2)
        opt.step([g])
    assert abs(opt.params[0] - 2.0) < 0.4
    print("lamb self-test passed", opt.params[0])
