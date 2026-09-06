"""Cholesky decomposition for symmetric positive-definite matrices.

Complexity: O(n^3).
Returns lower-triangular L such that A = L @ L.T.
Raises on non-SPD input. Original implementation.
"""
from __future__ import annotations

import numpy as np


def cholesky(A: np.ndarray) -> np.ndarray:
    """Return lower-triangular Cholesky factor of SPD matrix A."""
    A = np.array(A, dtype=float)
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError("A must be square")
    L = np.zeros_like(A)
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i, k] * L[j, k] for k in range(j))
            if i == j:
                val = A[i, i] - s
                if val <= 0:
                    raise np.linalg.LinAlgError("matrix not positive-definite")
                L[i, j] = np.sqrt(val)
            else:
                L[i, j] = (A[i, j] - s) / L[j, j]
    return L


if __name__ == "__main__":
    A = np.array([[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]])
    L = cholesky(A)
    assert np.allclose(L @ L.T, A)
    # identity
    I = np.eye(3)
    assert np.allclose(cholesky(I), I)
    try:
        cholesky(np.array([[1.0, 2.0], [2.0, 1.0]]))  # not PD
        assert False
    except np.linalg.LinAlgError:
        pass
    print("cholesky self-tests passed")
