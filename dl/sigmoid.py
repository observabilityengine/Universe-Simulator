"""Sigmoid activation."""
from __future__ import annotations
import math
from .tensor import Tensor


def sigmoid(x: Tensor) -> Tensor:
    r, c = x.shape
    data = [[1.0 / (1.0 + math.exp(-x.data[i][j])) for j in range(c)] for i in range(r)]
    out = Tensor(data, requires_grad=x.requires_grad, _parents=(x,), _op="sigmoid")
    def _backward():
        if x.requires_grad:
            if x.grad is None: x.grad = x._zeros()
            for i in range(r):
                for j in range(c):
                    s = out.data[i][j]
                    x.grad[i][j] += s * (1 - s) * out.grad[i][j]
    out._backward = _backward
    return out


if __name__ == "__main__":
    t = Tensor([[0.0]], requires_grad=True)
    y = sigmoid(t)
    assert abs(y.data[0][0] - 0.5) < 1e-6
    print("sigmoid self-tests passed")
