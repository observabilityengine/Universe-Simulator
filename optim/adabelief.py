"""
Universe Simulator - AdaBelief Optimizer
Original adaptive belief optimizer.
"""

from __future__ import annotations

import math
from typing import List

class AdaBelief:
    def __init__(self, params: List[float], lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [0.0] * len(params)
        self.s = [0.0] * len(params)
        self.t = 0

    def step(self, grads: List[float]) -> None:
        self.t += 1
        for i, g in enumerate(grads):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.s[i] = self.beta2 * self.s[i] + (1 - self.beta2) * (g - self.m[i]) ** 2
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            s_hat = self.s[i] / (1 - self.beta2 ** self.t)
            self.params[i] -= self.lr * m_hat / (math.sqrt(s_hat) + self.eps)

if __name__ == "__main__":
    opt = AdaBelief([0.0], lr=0.1)
    for _ in range(120):
        x = opt.params[0]
        g = 2 * (x - 3)
        opt.step([g])
    assert abs(opt.params[0] - 3.0) < 0.3
    print("adabelief self-test passed", opt.params[0])
