"""QR algorithm for eigenvalues of a real matrix (basic Francis QR).

Complexity: O(n^3 * iters). Original implementation with Gram-Schmidt QR.
"""
from __future__ import annotations
import math
from typing import List, Tuple

def _matmat(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    n, m, p = len(A), len(A[0]), len(B[0])
    C = [[0.0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            for j in range(p):
                C[i][j] += aik * B[k][j]
    return C

def _norm(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def _qr_gram_schmidt(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    n = len(A)
    m = len(A[0])
    Q = [[0.0] * m for _ in range(n)]
    R = [[0.0] * m for _ in range(m)]
    for j in range(m):
        v = [A[i][j] for i in range(n)]
        for i in range(j):
            R[i][j] = sum(Q[k][i] * A[k][j] for k in range(n))
            for k in range(n):
                v[k] -= R[i][j] * Q[k][i]
        R[j][j] = _norm(v)
        if R[j][j] > 1e-15:
            for k in range(n):
                Q[k][j] = v[k] / R[j][j]
    return Q, R

def qr_eigenvalues(A: List[List[float]], max_iter: int = 200, tol: float = 1e-10) -> List[float]:
    n = len(A)
    M = [row[:] for row in A]
    for _ in range(max_iter):
        Q, R = _qr_gram_schmidt(M)
        M = _matmat(R, Q)
        off = sum(abs(M[i][j]) for i in range(n) for j in range(n) if i != j)
        if off < tol:
            break
    return [M[i][i] for i in range(n)]

if __name__ == "__main__":
    A = [[2.0, 1.0], [1.0, 2.0]]
    ev = sorted(qr_eigenvalues(A, max_iter=50), reverse=True)
    assert abs(ev[0] - 3.0) < 1e-5
    assert abs(ev[1] - 1.0) < 1e-5
    print("qr_algorithm self-tests passed")
