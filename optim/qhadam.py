"""
Universe Simulator - QHAdam (Quasi-Hyperbolic Adam)
Original implementation.
"""

from __future__ import annotations

import math
from typing import List

class QHAdam:
    def __init__(self, params: List[float], lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.999,
                 nu1: float = 0.7, nu2: float = 1.0, eps: float = 1e-8):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.nu1 = nu1
        self.nu2 = nu2
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
            m_qh = self.nu1 * m_hat + (1 - self.nu1) * g
            v_qh = self.nu2 * v_hat + (1 - self.nu2) * g * g
            self.params[i] -= self.lr * m_qh / (math.sqrt(v_qh) + self.eps)

if __name__ == "__main__":
    opt = QHAdam([0.0], lr=0.1)
    for _ in range(100):
        x = opt.params[0]
        g = 2 * (x - 3.5)
        opt.step([g])
    assert abs(opt.params[0] - 3.5) < 0.3
    print("qhadam self-test passed", opt.params[0])
