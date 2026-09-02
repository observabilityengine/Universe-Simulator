"""
Module 62 – QR Decomposition
Classical Gram-Schmidt QR factorization.
Complete implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Tuple


def qr_decompose(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    A = np.array(A, dtype=float, copy=True)
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            R[i, j] = Q[:, i] @ A[:, j]
            v -= R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        if R[j, j] < 1e-15:
            raise np.linalg.LinAlgError("Linearly dependent columns")
        Q[:, j] = v / R[j, j]
    return Q, R


def qr_solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    Q, R = qr_decompose(A)
    y = Q.T @ b
    n = R.shape[0]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - R[i, i + 1 :] @ x[i + 1 :]) / R[i, i]
    return x


if __name__ == "__main__":
    print("Testing QR Decomposition...")
    A = np.array([[12.0, -51.0, 4.0], [6.0, 167.0, -68.0], [-4.0, 24.0, -41.0]])
    Q, R = qr_decompose(A)
    print(f"  Q orthogonal residual: {np.max(np.abs(Q.T @ Q - np.eye(3))):.2e}")
    print(f"  A - QR residual: {np.max(np.abs(A - Q @ R)):.2e}")
    b = np.array([1.0, 2.0, 3.0])
    x = qr_solve(A, b)
    print(f"  Solve residual: {np.max(np.abs(A @ x - b)):.2e}")
    print("QR Decomposition module OK.")
