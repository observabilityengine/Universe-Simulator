"""
Universe Simulator - Nesterov Accelerated Gradient
Original implementation.
"""

from __future__ import annotations

from typing import List

class Nesterov:
    def __init__(self, params: List[float], lr: float = 0.01, mu: float = 0.9):
        self.params = list(params)
        self.lr = lr
        self.mu = mu
        self.v = [0.0] * len(params)

    def step(self, grad_fn) -> None:
        # lookahead
        lookahead = [p + self.mu * vv for p, vv in zip(self.params, self.v)]
        grads = grad_fn(lookahead)
        for i, g in enumerate(grads):
            self.v[i] = self.mu * self.v[i] - self.lr * g
            self.params[i] += self.v[i]

if __name__ == "__main__":
    opt = Nesterov([0.0], lr=0.05, mu=0.9)
    def grad(params):
        return [2 * (params[0] - 3)]
    for _ in range(100):
        opt.step(grad)
    assert abs(opt.params[0] - 3.0) < 0.2
    print("nesterov self-test passed", opt.params[0])
