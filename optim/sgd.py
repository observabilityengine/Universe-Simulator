"""
Universe Simulator - Vanilla SGD
Original stochastic gradient descent.
"""

from __future__ import annotations

from typing import List


class SGD:
    def __init__(self, params: List[float], lr: float = 0.01):
        self.params = list(params)
        self.lr = lr

    def step(self, grads: List[float]) -> None:
        for i, g in enumerate(grads):
            self.params[i] -= self.lr * g


if __name__ == "__main__":
    opt = SGD([0.0], lr=0.1)
    for _ in range(100):
        x = opt.params[0]
        g = 2 * (x - 4)
        opt.step([g])
    assert abs(opt.params[0] - 4.0) < 0.1
    print("sgd self-test passed", opt.params[0])
