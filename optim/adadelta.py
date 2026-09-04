"""
Universe Simulator - AdaDelta Optimizer
Original implementation.
"""

from __future__ import annotations

from typing import List

class AdaDelta:
    def __init__(self, params: List[float], rho: float = 0.95, eps: float = 1e-6):
        self.params = list(params)
        self.rho = rho
        self.eps = eps
        self.eg2 = [0.0] * len(params)
        self.edx2 = [0.0] * len(params)

    def step(self, grads: List[float]) -> None:
        for i, g in enumerate(grads):
            self.eg2[i] = self.rho * self.eg2[i] + (1 - self.rho) * g * g
            dx = -math.sqrt(self.edx2[i] + self.eps) / math.sqrt(self.eg2[i] + self.eps) * g
            self.edx2[i] = self.rho * self.edx2[i] + (1 - self.rho) * dx * dx
            self.params[i] += dx

import math

if __name__ == "__main__":
    opt = AdaDelta([0.0])
    for _ in range(200):
        x = opt.params[0]
        g = 2 * (x - 2.5)
        opt.step([g])
    assert abs(opt.params[0] - 2.5) < 0.3
    print("adadelta self-test passed", opt.params[0])
