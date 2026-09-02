"""
Universe Simulator - PCA via power iteration (first component)
Original covariance + power method.
"""

from __future__ import annotations

from typing import List, Tuple


def _mat_vec(A: List[List[float]], v: List[float]) -> List[float]:
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _norm(v: List[float]) -> float:
    return sum(x * x for x in v) ** 0.5


def pca_first(data: List[List[float]], iters: int = 50) -> Tuple[List[float], float]:
    """Return first principal component and eigenvalue estimate."""
    n = len(data)
    d = len(data[0])
    mean = [sum(row[j] for row in data) / n for j in range(d)]
    centered = [[row[j] - mean[j] for j in range(d)] for row in data]
    # covariance
    cov = [[0.0] * d for _ in range(d)]
    for row in centered:
        for i in range(d):
            for j in range(d):
                cov[i][j] += row[i] * row[j]
    for i in range(d):
        for j in range(d):
            cov[i][j] /= max(n - 1, 1)
    # power iteration
    v = [1.0 / d] * d
    for _ in range(iters):
        v = _mat_vec(cov, v)
        nrm = _norm(v) or 1.0
        v = [x / nrm for x in v]
    # Rayleigh
    Av = _mat_vec(cov, v)
    lam = sum(v[i] * Av[i] for i in range(d))
    return v, lam


if __name__ == "__main__":
    data = [[1.0, 2.0], [2.0, 4.0], [3.0, 6.0], [4.0, 8.1]]
    vec, eig = pca_first(data)
    assert abs(vec[0]) > 0.4 and abs(vec[1]) > 0.4
    print("pca self-test passed", vec, eig)
