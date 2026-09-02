"""
Universe Simulator - RMSProp
Original implementation.
"""

from __future__ import annotations

from typing import List


class RMSProp:
    def __init__(self, params: List[float], lr: float = 0.01, decay: float = 0.9, eps: float = 1e-8):
        self.params = list(params)
        self.lr = lr
        self.decay = decay
        self.eps = eps
        self.sq = [0.0] * len(params)

    def step(self, grads: List[float]) -> None:
        for i, g in enumerate(grads):
            self.sq[i] = self.decay * self.sq[i] + (1 - self.decay) * g * g
            self.params[i] -= self.lr * g / (self.sq[i] ** 0.5 + self.eps)


if __name__ == "__main__":
    opt = RMSProp([0.0], lr=0.1)
    for _ in range(200):
        x = opt.params[0]
        g = 2 * (x - 5)
        opt.step([g])
    assert abs(opt.params[0] - 5.0) < 0.15
    print("rmsprop self-test passed", opt.params[0])
