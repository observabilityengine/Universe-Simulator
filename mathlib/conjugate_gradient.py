"""Conjugate gradient solver for SPD linear systems Ax = b.

Complexity: O(n^2) per iteration typical; converges in ≤ n steps for exact arith.
Requires A symmetric positive-definite. Original implementation.
"""
from __future__ import annotations

import numpy as np


def conjugate_gradient(
    A: np.ndarray,
    b: np.ndarray,
    tol: float = 1e-10,
    max_iter: int | None = None,
) -> np.ndarray:
    """Solve Ax = b via CG. Returns x."""
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    n = b.shape[0]
    if A.shape != (n, n):
        raise ValueError("A must be n×n matching b")
    if max_iter is None:
        max_iter = n * 2
    x = np.zeros(n)
    r = b - A @ x
    p = r.copy()
    rs_old = np.dot(r, r)
    if rs_old < tol * tol:
        return x
    for _ in range(max_iter):
        Ap = A @ p
        alpha = rs_old / np.dot(p, Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        rs_new = np.dot(r, r)
        if rs_new < tol * tol:
            break
        p = r + (rs_new / rs_old) * p
        rs_old = rs_new
    return x


if __name__ == "__main__":
    A = np.array([[4.0, 1.0], [1.0, 3.0]])
    b = np.array([1.0, 2.0])
    x = conjugate_gradient(A, b)
    assert np.allclose(A @ x, b, atol=1e-8)
    I = np.eye(5)
    b2 = np.arange(5, dtype=float)
    assert np.allclose(conjugate_gradient(I, b2), b2)
    print("conjugate_gradient self-tests passed")
