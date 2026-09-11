"""Autograd utilities and gradient checking."""
from __future__ import annotations
from typing import Callable
from .tensor import Tensor


def grad_check(fn: Callable, x: Tensor, eps: float = 1e-5) -> float:
    """Compare analytic vs numerical gradient for scalar output."""
    x.requires_grad = True
    out = fn(x)
    out.backward()
    analytic = [row[:] for row in x.grad]
    numerical = x._zeros()
    r, c = x.shape
    for i in range(r):
        for j in range(c):
            x.data[i][j] += eps
            plus = fn(x).data[0][0]
            x.data[i][j] -= 2 * eps
            minus = fn(x).data[0][0]
            x.data[i][j] += eps
            numerical[i][j] = (plus - minus) / (2 * eps)
    diff = 0.0
    for i in range(r):
        for j in range(c):
            diff += abs(analytic[i][j] - numerical[i][j])
    return diff


if __name__ == "__main__":
    from .tensor import Tensor
    def f(t):
        return (t * t).sum()
    x = Tensor([[1.0, 2.0]], requires_grad=True)
    d = grad_check(f, x)
    assert d < 1e-4
    print(f"autograd grad_check diff={d:.2e}")
    print("autograd self-tests passed")
