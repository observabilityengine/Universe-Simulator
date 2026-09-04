"""
Universe Simulator - Lion Optimizer
Original sign-based momentum optimizer.
"""

from __future__ import annotations

from typing import List

class Lion:
    def __init__(self, params: List[float], lr: float = 1e-4, beta1: float = 0.9, beta2: float = 0.99):
        self.params = list(params)
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.m = [0.0] * len(params)

    def step(self, grads: List[float]) -> None:
        for i, g in enumerate(grads):
            c = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.params[i] -= self.lr * (1.0 if c > 0 else -1.0 if c < 0 else 0.0)
            self.m[i] = self.beta2 * self.m[i] + (1 - self.beta2) * g

if __name__ == "__main__":
    opt = Lion([0.0], lr=0.1)
    for _ in range(50):
        x = opt.params[0]
        g = 2 * (x - 2)
        opt.step([g])
    assert abs(opt.params[0] - 2.0) < 0.5
    print("lion self-test passed", opt.params[0])
