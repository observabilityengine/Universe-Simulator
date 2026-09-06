"""LU decomposition with partial pivoting (Doolittle).

Complexity: O(n^3).
Returns (P, L, U) such that P @ A = L @ U.
Original implementation.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def lu_decomposition(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return permutation P, lower L, upper U with P @ A = L @ U."""
    A = np.array(A, dtype=float, copy=True)
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError("A must be square")
    P = np.eye(n)
    L = np.eye(n)
    U = A.copy()
    for k in range(n - 1):
        pivot = k + np.argmax(np.abs(U[k:, k]))
        if abs(U[pivot, k]) < 1e-14:
            raise np.linalg.LinAlgError("singular matrix")
        if pivot != k:
            U[[k, pivot]] = U[[pivot, k]]
            P[[k, pivot]] = P[[pivot, k]]
            if k > 0:
                L[[k, pivot], :k] = L[[pivot, k], :k]
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
            U[i, k] = 0.0
    return P, L, U


if __name__ == "__main__":
    A = np.array([[2.0, 1.0, 1.0], [4.0, -6.0, 0.0], [-2.0, 7.0, 2.0]])
    P, L, U = lu_decomposition(A)
    assert np.allclose(P @ A, L @ U)
    assert np.allclose(np.tril(L), L) and np.allclose(np.triu(U), U)
    I = np.eye(4)
    P2, L2, U2 = lu_decomposition(I)
    assert np.allclose(L2 @ U2, I)
    print("lu_decomposition self-tests passed")
