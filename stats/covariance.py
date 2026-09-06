"""Sample and population covariance / covariance matrix.

Complexity: O(n) for two series; O(n d^2) for d-dimensional matrix.
Original implementation.
"""
from __future__ import annotations

from typing import Sequence
import numpy as np


def covariance(x: Sequence[float], y: Sequence[float], sample: bool = True) -> float:
    n = len(x)
    if n != len(y) or n < 1:
        raise ValueError("equal non-empty sequences required")
    if sample and n < 2:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    c = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    return c / (n - 1) if sample else c / n


def covariance_matrix(X: np.ndarray, sample: bool = True) -> np.ndarray:
    """X shape (n_samples, n_features)."""
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError("X must be 2-D")
    n = X.shape[0]
    Xc = X - X.mean(axis=0)
    denom = n - 1 if sample and n > 1 else max(n, 1)
    return (Xc.T @ Xc) / denom


if __name__ == "__main__":
    x = [1.0, 2.0, 3.0, 4.0]
    y = [2.0, 4.0, 6.0, 8.0]
    assert abs(covariance(x, y) - 3.333333) < 1e-5
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    C = covariance_matrix(X)
    assert C.shape == (2, 2)
    assert abs(C[0, 1] - C[1, 0]) < 1e-12
    print("covariance self-tests passed")
