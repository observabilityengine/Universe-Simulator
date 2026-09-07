"""Principal Component Analysis via SVD of the covariance matrix.

Complexity: O(min(n d^2, d n^2)). Original implementation using pure Python + math.
"""
from __future__ import annotations

import math
from typing import List, Tuple


def _dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _norm(v: List[float]) -> float:
    return math.sqrt(_dot(v, v))


def _matvec(A: List[List[float]], x: List[float]) -> List[float]:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def _power_iteration(A: List[List[float]], num_iter: int = 100) -> Tuple[float, List[float]]:
    n = len(A)
    v = [1.0 / math.sqrt(n)] * n
    for _ in range(num_iter):
        Av = _matvec(A, v)
        norm = _norm(Av)
        if norm < 1e-15:
            break
        v = [x / norm for x in Av]
    Av = _matvec(A, v)
    lam = _dot(v, Av)
    return lam, v


def _deflate(A: List[List[float]], lam: float, v: List[float]) -> None:
    n = len(A)
    for i in range(n):
        for j in range(n):
            A[i][j] -= lam * v[i] * v[j]


def pca(
    X: List[List[float]], n_components: int,
) -> Tuple[List[List[float]], List[float], List[List[float]]]:
    n = len(X)
    d = len(X[0])
    assert 1 <= n_components <= min(n, d)
    mean = [sum(X[i][j] for i in range(n)) / n for j in range(d)]
    Xc = [[X[i][j] - mean[j] for j in range(d)] for i in range(n)]
    cov = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            cov[i][j] = sum(Xc[k][i] * Xc[k][j] for k in range(n)) / max(1, n - 1)
    components: List[List[float]] = []
    variances: List[float] = []
    A = [row[:] for row in cov]
    for _ in range(n_components):
        lam, v = _power_iteration(A)
        components.append(v)
        variances.append(max(lam, 0.0))
        _deflate(A, lam, v)
    transformed = [[_dot(row, comp) for comp in components] for row in Xc]
    return transformed, variances, components


if __name__ == "__main__":
    X = [[float(i), 2.0 * i + 0.01 * (i % 3)] for i in range(20)]
    Z, var, comps = pca(X, n_components=1)
    assert len(Z) == 20 and len(Z[0]) == 1
    c = comps[0]
    ratio = abs(c[1] / c[0]) if abs(c[0]) > 1e-8 else 999
    assert 1.5 < ratio < 2.5, ratio
    assert var[0] > 0
    print("pca self-tests passed")
