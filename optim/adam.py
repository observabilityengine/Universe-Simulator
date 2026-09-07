"""Adam optimizer.

Complexity: O(iters * dim). Original implementation.
"""
from __future__ import annotations

from typing import Callable, List, Tuple
import math


def adam(
    f: Callable[[List[float]], float],
    grad: Callable[[List[float]], List[float]],
    x0: List[float],
    lr: float = 0.01,
    betas: Tuple[float, float] = (0.9, 0.999),
    eps: float = 1e-8,
    max_iter: int = 1000,
    tol: float = 1e-6,
) -> Tuple[List[float], float]:
    x = x0[:]
    m = [0.0] * len(x)
    v = [0.0] * len(x)
    beta1, beta2 = betas
    for t in range(1, max_iter + 1):
        g = grad(x)
        gnorm = math.sqrt(sum(gi * gi for gi in g))
        if gnorm < tol:
            break
        for i in range(len(x)):
            m[i] = beta1 * m[i] + (1 - beta1) * g[i]
            v[i] = beta2 * v[i] + (1 - beta2) * g[i] * g[i]
            mhat = m[i] / (1 - beta1 ** t)
            vhat = v[i] / (1 - beta2 ** t)
            x[i] -= lr * mhat / (math.sqrt(vhat) + eps)
    return x, f(x)


if __name__ == "__main__":
    def rosen(x):
        return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2

    def rosen_grad(x):
        d0 = -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0] ** 2)
        d1 = 200 * (x[1] - x[0] ** 2)
        return [d0, d1]

    x, v = adam(rosen, rosen_grad, [-1.0, 1.0], lr=0.05, max_iter=3000)
    assert v < 0.1, v
    print("adam self-tests passed")
