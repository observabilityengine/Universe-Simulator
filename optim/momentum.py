"""
Universe Simulator - SGD with Momentum
Original implementation.
"""

from __future__ import annotations

from typing import List


class MomentumSGD:
    def __init__(self, params: List[float], lr: float = 0.01, mu: float = 0.9):
        self.params = list(params)
        self.lr = lr
        self.mu = mu
        self.v = [0.0] * len(params)

    def step(self, grads: List[float]) -> None:
        for i, g in enumerate(grads):
            self.v[i] = self.mu * self.v[i] - self.lr * g
            self.params[i] += self.v[i]


if __name__ == "__main__":
    opt = MomentumSGD([0.0], lr=0.05, mu=0.9)
    for _ in range(150):
        x = opt.params[0]
        g = 2 * (x - 4)
        opt.step([g])
    assert abs(opt.params[0] - 4.0) < 0.15
    print("momentum self-test passed", opt.params[0])
