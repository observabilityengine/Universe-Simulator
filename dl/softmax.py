"""Softmax activation."""
from __future__ import annotations
import math
from .tensor import Tensor


def softmax(x: Tensor) -> Tensor:
    r, c = x.shape
    data = []
    for i in range(r):
        row = x.data[i]
        m = max(row)
        exps = [math.exp(v - m) for v in row]
        s = sum(exps) or 1.0
        data.append([e / s for e in exps])
    out = Tensor(data, requires_grad=x.requires_grad, _parents=(x,), _op="softmax")
    def _backward():
        if x.requires_grad:
            if x.grad is None: x.grad = x._zeros()
            for i in range(r):
                for j in range(c):
                    for k in range(c):
                        delta = (1.0 if j == k else 0.0) - out.data[i][k]
                        x.grad[i][j] += out.data[i][j] * delta * out.grad[i][k]
    out._backward = _backward
    return out


if __name__ == "__main__":
    t = Tensor([[1.0, 2.0, 3.0]])
    y = softmax(t)
    assert abs(sum(y.data[0]) - 1.0) < 1e-6
    print(f"softmax {y.data[0]}")
    print("softmax self-tests passed")
