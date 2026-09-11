"""Dropout regularization."""
from __future__ import annotations
import random
from .tensor import Tensor


class Dropout:
    def __init__(self, p: float = 0.5, seed: int = 42):
        self.p = p
        self.training = True
        self.rng = random.Random(seed)

    def __call__(self, x: Tensor) -> Tensor:
        if not self.training or self.p == 0:
            return x
        r, c = x.shape
        mask = [[1.0 if self.rng.random() > self.p else 0.0 for _ in range(c)] for _ in range(r)]
        scale = 1.0 / (1.0 - self.p)
        data = [[x.data[i][j] * mask[i][j] * scale for j in range(c)] for i in range(r)]
        out = Tensor(data, requires_grad=x.requires_grad, _parents=(x,), _op="dropout")
        def _backward():
            if x.requires_grad:
                if x.grad is None: x.grad = x._zeros()
                for i in range(r):
                    for j in range(c):
                        x.grad[i][j] += mask[i][j] * scale * out.grad[i][j]
        out._backward = _backward
        return out

    def parameters(self):
        return []


if __name__ == "__main__":
    d = Dropout(0.5, seed=1)
    x = Tensor([[1.0] * 10], requires_grad=True)
    y = d(x)
    assert y.shape == (1, 10)
    print("dropout self-tests passed")
