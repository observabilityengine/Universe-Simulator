"""Householder QR factorization (thin QR for tall matrices).

Complexity: O(m n^2). Original implementation.
"""
from __future__ import annotations
import math
from typing import List, Tuple


def qr_householder(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Return Q, R such that A = Q R. A is m x n with m >= n."""
    m = len(A)
    n = len(A[0])
    # Work on a copy
    R = [row[:] for row in A]
    Q = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]

    for k in range(n):
        # Householder vector for column k from row k downward
        x = [R[i][k] for i in range(k, m)]
        normx = math.sqrt(sum(v * v for v in x))
        if normx < 1e-15:
            continue
        sign = 1.0 if x[0] >= 0 else -1.0
        u1 = x[0] + sign * normx
        v = [u1] + x[1:]
        beta = 2.0 / sum(vi * vi for vi in v)
        # Apply to R
        for j in range(k, n):
            s = sum(v[i - k] * R[i][j] for i in range(k, m))
            for i in range(k, m):
                R[i][j] -= beta * v[i - k] * s
        # Accumulate Q (apply to identity from the left)
        for j in range(m):
            s = sum(v[i - k] * Q[i][j] for i in range(k, m))
            for i in range(k, m):
                Q[i][j] -= beta * v[i - k] * s

    # Q is currently Q^T; transpose it
    Q = [[Q[j][i] for j in range(m)] for i in range(m)]
    # Thin: take first n columns of Q, first n rows of R
    Q_thin = [row[:n] for row in Q]
    R_thin = [R[i][:n] for i in range(n)]
    return Q_thin, R_thin


if __name__ == "__main__":
    A = [[1.0, 1.0], [1.0, 0.0], [0.0, 1.0]]
    Q, R = qr_householder(A)
    # Reconstruct
    recon = [[sum(Q[i][k] * R[k][j] for k in range(2)) for j in range(2)] for i in range(3)]
    err = sum((recon[i][j] - A[i][j]) ** 2 for i in range(3) for j in range(2)) ** 0.5
    assert err < 1e-10, err
    # Q columns orthonormal
    dot = sum(Q[i][0] * Q[i][1] for i in range(3))
    assert abs(dot) < 1e-10
    print("qr_householder self-tests passed")
