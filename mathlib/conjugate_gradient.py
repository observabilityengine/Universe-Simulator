"""Conjugate Gradient method for symmetric positive-definite linear systems.

Complexity: O(k * n^2) for k iterations. Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple
import math


def conjugate_gradient(
    A: List[List[float]],
    b: List[float],
    x0: List[float] | None = None,
    tol: float = 1e-8,
    max_iter: int | None = None,
) -> Tuple[List[float], int]:
    """Solve A x = b for SPD matrix A. Returns (x, iterations)."""
    n = len(b)
    if max_iter is None:
        max_iter = n * 2
    x = x0[:] if x0 is not None else [0.0] * n

    def matvec(v: List[float]) -> List[float]:
        return [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]

    r = [b[i] - matvec(x)[i] for i in range(n)]
    p = r[:]
    rsold = sum(ri * ri for ri in r)

    for k in range(max_iter):
        Ap = matvec(p)
        pAp = sum(p[i] * Ap[i] for i in range(n))
        if abs(pAp) < 1e-18:
            break
        alpha = rsold / pAp
        x = [x[i] + alpha * p[i] for i in range(n)]
        r = [r[i] - alpha * Ap[i] for i in range(n)]
        rsnew = sum(ri * ri for ri in r)
        if math.sqrt(rsnew) < tol:
            return x, k + 1
        beta = rsnew / rsold
        p = [r[i] + beta * p[i] for i in range(n)]
        rsold = rsnew
    return x, max_iter


if __name__ == "__main__":
    A = [[4.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
    b = [1.0, 2.0, 3.0]
    x, iters = conjugate_gradient(A, b, tol=1e-10)
    residual = [b[i] - sum(A[i][j] * x[j] for j in range(3)) for i in range(3)]
    assert all(abs(r) < 1e-8 for r in residual), residual
    assert iters < 10
    print("conjugate_gradient self-tests passed")
