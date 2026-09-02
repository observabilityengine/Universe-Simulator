"""
Universe Simulator - AdaGrad Optimizer
Original implementation.
"""

from __future__ import annotations

from typing import List


class AdaGrad:
    def __init__(self, params: List[float], lr: float = 0.1, eps: float = 1e-8):
        self.params = list(params)
        self.lr = lr
        self.eps = eps
        self.g2 = [0.0] * len(params)

    def step(self, grads: List[float]) -> None:
        for i, g in enumerate(grads):
            self.g2[i] += g * g
            self.params[i] -= self.lr * g / (self.g2[i] ** 0.5 + self.eps)


if __name__ == "__main__":
    opt = AdaGrad([0.0], lr=1.0)
    for _ in range(100):
        x = opt.params[0]
        g = 2 * (x - 3)
        opt.step([g])
    assert abs(opt.params[0] - 3.0) < 0.2
    print("adagrad self-test passed", opt.params[0])
