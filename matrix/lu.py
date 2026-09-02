"""
Module 55 – LU Decomposition
Doolittle LU factorization with partial pivoting + solver.
Complete implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Tuple


def lu_decompose(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    A = np.array(A, dtype=float, copy=True)
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix must be square")
    L = np.eye(n)
    U = np.zeros((n, n))
    P = np.eye(n)

    for k in range(n):
        max_row = np.argmax(np.abs(A[k:, k])) + k
        if abs(A[max_row, k]) < 1e-15:
            raise np.linalg.LinAlgError("Matrix is singular")
        if max_row != k:
            A[[k, max_row]] = A[[max_row, k]]
            P[[k, max_row]] = P[[max_row, k]]
            if k > 0:
                L[[k, max_row], :k] = L[[max_row, k], :k]
        for i in range(k + 1, n):
            L[i, k] = A[i, k] / A[k, k]
            A[i, k:] -= L[i, k] * A[k, k:]
        U[k, k:] = A[k, k:]
    return P, L, U


def lu_solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    P, L, U = lu_decompose(A)
    Pb = P @ b
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = Pb[i] - L[i, :i] @ y[:i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1 :] @ x[i + 1 :]) / U[i, i]
    return x


if __name__ == "__main__":
    print("Testing LU Decomposition...")
    A = np.array([[2.0, 1.0, 1.0], [4.0, -6.0, 0.0], [-2.0, 7.0, 2.0]])
    b = np.array([5.0, -2.0, 9.0])
    P, L, U = lu_decompose(A)
    print(f"  P@A - L@U residual: {np.max(np.abs(P @ A - L @ U)):.2e}")
    x = lu_solve(A, b)
    print(f"  Solution x: {x}")
    print(f"  A@x residual: {np.max(np.abs(A @ x - b)):.2e}")
    print("LU Decomposition module OK.")
