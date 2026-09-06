"""QR decomposition via classical Gram-Schmidt.

Complexity: O(m n^2) for m×n matrix with m >= n.
Returns Q (orthonormal columns), R (upper triangular) with A = Q @ R.
Original implementation.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def qr_decomposition(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Thin QR of A (m×n, m>=n) via classical Gram-Schmidt."""
    A = np.array(A, dtype=float)
    m, n = A.shape
    if m < n:
        raise ValueError("m >= n required for thin QR")
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            v -= R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        if R[j, j] < 1e-14:
            raise np.linalg.LinAlgError("rank-deficient matrix")
        Q[:, j] = v / R[j, j]
    return Q, R


if __name__ == "__main__":
    A = np.array([[1.0, 1.0], [1.0, 0.0], [0.0, 1.0]])
    Q, R = qr_decomposition(A)
    assert np.allclose(Q @ R, A)
    assert np.allclose(Q.T @ Q, np.eye(2), atol=1e-10)
    assert np.allclose(np.triu(R), R)
    I = np.eye(3)
    Q2, R2 = qr_decomposition(I)
    assert np.allclose(Q2 @ R2, I)
    print("qr_decomposition self-tests passed")
