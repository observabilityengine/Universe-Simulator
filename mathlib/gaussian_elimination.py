"""Gaussian elimination with partial pivoting for linear systems.

Complexity: O(n^3).
Solves Ax = b for square A. Returns solution or raises on singular.
"""
from __future__ import annotations

import numpy as np


def gaussian_elimination(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve Ax = b. A must be square, b 1-D of length n."""
    A = np.array(A, dtype=float, copy=True)
    b = np.array(b, dtype=float, copy=True)
    n = A.shape[0]
    if A.shape != (n, n) or b.shape != (n,):
        raise ValueError("A square, b length n required")

    for k in range(n - 1):
        max_row = k + np.argmax(np.abs(A[k:, k]))
        if abs(A[max_row, k]) < 1e-14:
            raise np.linalg.LinAlgError("singular matrix")
        if max_row != k:
            A[[k, max_row]] = A[[max_row, k]]
            b[[k, max_row]] = b[[max_row, k]]
        for i in range(k + 1, n):
            factor = A[i, k] / A[k, k]
            A[i, k:] -= factor * A[k, k:]
            b[i] -= factor * b[k]

    if abs(A[n - 1, n - 1]) < 1e-14:
        raise np.linalg.LinAlgError("singular matrix")

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]
    return x


if __name__ == "__main__":
    A = np.array([[2., 1.], [1., 3.]])
    b = np.array([4., 5.])
    x = gaussian_elimination(A, b)
    assert np.allclose(x, np.linalg.solve(A, b))
    I = np.eye(4)
    b = np.arange(4.)
    assert np.allclose(gaussian_elimination(I, b), b)
    try:
        gaussian_elimination(np.array([[1., 2.], [2., 4.]]), np.array([1., 2.]))
        assert False
    except np.linalg.LinAlgError:
        pass
    assert abs(gaussian_elimination(np.array([[5.]]), np.array([10.]))[0] - 2.) < 1e-12
    print("gaussian_elimination self-tests passed")
