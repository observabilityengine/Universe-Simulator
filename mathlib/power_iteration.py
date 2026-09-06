"""Power iteration for dominant eigenvalue / eigenvector.

Complexity: O(k n^2) for k iterations on n×n matrix.
Returns (eigenvalue, eigenvector). Assumes unique dominant eigenvalue.
Original implementation.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def power_iteration(
    A: np.ndarray,
    num_iter: int = 100,
    tol: float = 1e-12,
    seed: int | None = None,
) -> Tuple[float, np.ndarray]:
    """Estimate dominant eigenpair of A."""
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError("A must be square")
    rng = np.random.default_rng(seed)
    b = rng.normal(size=n)
    b /= np.linalg.norm(b)
    eigenvalue = 0.0
    for _ in range(num_iter):
        b_new = A @ b
        norm = np.linalg.norm(b_new)
        if norm < 1e-15:
            return 0.0, b_new
        b_new /= norm
        eigenvalue = float(b_new @ A @ b_new)
        if np.linalg.norm(b_new - b) < tol or np.linalg.norm(b_new + b) < tol:
            b = b_new
            break
        b = b_new
    return eigenvalue, b


if __name__ == "__main__":
    A = np.array([[2.0, 0.0], [0.0, 1.0]])
    val, vec = power_iteration(A, num_iter=50, seed=0)
    assert abs(val - 2.0) < 1e-6
    assert abs(abs(vec[0]) - 1.0) < 1e-5
    # rank-1
    v = np.array([1.0, 2.0, 3.0])
    A2 = np.outer(v, v)
    val2, _ = power_iteration(A2, num_iter=80, seed=1)
    assert abs(val2 - np.dot(v, v)) < 1e-4
    print("power_iteration self-tests passed")
