"""Strassen matrix multiplication.

Complexity: O(n^{log2 7}) ≈ O(n^2.807) for n power of 2.
Falls back to classic for small n or non-power-of-2 (pad).
"""
from __future__ import annotations

import numpy as np


def strassen(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Multiply two square matrices via Strassen (pad to power of 2)."""
    if A.ndim != 2 or B.ndim != 2 or A.shape[0] != A.shape[1] or B.shape[0] != B.shape[1] or A.shape[1] != B.shape[0]:
        raise ValueError("square matrices of compatible size required")
    n = A.shape[0]
    m = 1
    while m < n:
        m <<= 1
    if m != n:
        Ap = np.zeros((m, m), dtype=A.dtype)
        Bp = np.zeros((m, m), dtype=B.dtype)
        Ap[:n, :n] = A
        Bp[:n, :n] = B
        Cp = _strassen_rec(Ap, Bp)
        return Cp[:n, :n]
    return _strassen_rec(A, B)


def _strassen_rec(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    if n <= 64:
        return A @ B
    mid = n // 2
    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    M1 = _strassen_rec(A11 + A22, B11 + B22)
    M2 = _strassen_rec(A21 + A22, B11)
    M3 = _strassen_rec(A11, B12 - B22)
    M4 = _strassen_rec(A22, B21 - B11)
    M5 = _strassen_rec(A11 + A12, B22)
    M6 = _strassen_rec(A21 - A11, B11 + B12)
    M7 = _strassen_rec(A12 - A22, B21 + B22)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    C = np.empty((n, n), dtype=A.dtype)
    C[:mid, :mid] = C11
    C[:mid, mid:] = C12
    C[mid:, :mid] = C21
    C[mid:, mid:] = C22
    return C


if __name__ == "__main__":
    A = np.array([[1., 2.], [3., 4.]])
    B = np.array([[5., 6.], [7., 8.]])
    C = strassen(A, B)
    assert np.allclose(C, A @ B)
    assert strassen(np.array([[3.]]), np.array([[4.]]))[0, 0] == 12.
    A0 = np.zeros((0, 0))
    assert strassen(A0, A0).shape == (0, 0)
    n = 8
    A = np.random.randn(n, n)
    B = np.random.randn(n, n)
    assert np.allclose(strassen(A, B), A @ B, atol=1e-8)
    A = np.random.randn(5, 5)
    B = np.random.randn(5, 5)
    assert np.allclose(strassen(A, B), A @ B, atol=1e-8)
    print("strassen self-tests passed")
