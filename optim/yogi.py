"""
Universe Simulator - Yogi Optimizer
Original adaptive optimizer with controlled second-moment growth.
"""

from __future__ import annotations

import math
from typing import List

class Yogi:
    def __init__(self, params: List[float], lr: float = 0.01, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-3):
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
            sign = 1.0 if (g * g - self.v[i]) > 0 else -1.0
            self.v[i] = self.v[i] + (1 - self.beta2) * sign * (g * g)
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            self.params[i] -= self.lr * m_hat / (math.sqrt(abs(self.v[i])) + self.eps)

if __name__ == "__main__":
    opt = Yogi([0.0], lr=0.1)
    for _ in range(120):
        x = opt.params[0]
        g = 2 * (x - 4)
        opt.step([g])
    assert abs(opt.params[0] - 4.0) < 0.3
    print("yogi self-test passed", opt.params[0])
