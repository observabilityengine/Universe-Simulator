"""
Universe Simulator - Sophia Optimizer (second-order diagonal)
Original simplified Hessian-aware update.
"""

from __future__ import annotations

import math
from typing import List

class Sophia:
    def __init__(self, params: List[float], lr: float = 0.001, beta1: float = 0.9, beta2: float = 0.99, eps: float = 1e-8, rho: float = 0.04):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.rho = rho
        self.m = [0.0] * len(params)
        self.h = [0.0] * len(params)
        self.t = 0

    def step(self, grads: List[float], hessian_diag: List[float] = None) -> None:
        self.t += 1
        if hessian_diag is None:
            hessian_diag = [g*g for g in grads]
        for i, g in enumerate(grads):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.h[i] = self.beta2 * self.h[i] + (1 - self.beta2) * hessian_diag[i]
            # clip
            update = self.m[i] / max(self.h[i], self.eps)
            update = max(-self.rho, min(self.rho, update))
            self.params[i] -= self.lr * update

if __name__ == "__main__":
    opt = Sophia([0.0], lr=0.1)
    for _ in range(80):
        x = opt.params[0]
        g = 2 * (x - 3)
        opt.step([g], [2.0])
    assert abs(opt.params[0] - 3.0) < 0.5
    print("sophia self-test passed", opt.params[0])
