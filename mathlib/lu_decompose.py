"""LU decomposition with partial pivoting.

Complexity: O(n^3). Original implementation.
"""
from __future__ import annotations
from typing import List, Tuple

def lu_decompose(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[int]]:
    n = len(A)
    U = [row[:] for row in A]
    L = [[0.0]*n for _ in range(n)]
    pivots = list(range(n))
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(U[i][k]))
        if abs(U[piv][k]) < 1e-15:
            raise ValueError("Singular matrix")
        if piv != k:
            U[k], U[piv] = U[piv], U[k]
            L[k], L[piv] = L[piv], L[k]
            pivots[k], pivots[piv] = pivots[piv], pivots[k]
        L[k][k] = 1.0
        for i in range(k+1, n):
            L[i][k] = U[i][k] / U[k][k]
            for j in range(k, n):
                U[i][j] -= L[i][k] * U[k][j]
    return L, U, pivots

def lu_solve(L: List[List[float]], U: List[List[float]], pivots: List[int], b: List[float]) -> List[float]:
    n = len(b)
    bp = [b[pivots[i]] for i in range(n)]
    y = [0.0]*n
    for i in range(n):
        y[i] = bp[i] - sum(L[i][j]*y[j] for j in range(i))
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(U[i][j]*x[j] for j in range(i+1, n))) / U[i][i]
    return x

if __name__ == "__main__":
    A = [[2.0, 1.0, 1.0], [4.0, -6.0, 0.0], [-2.0, 7.0, 2.0]]
    b = [5.0, -2.0, 9.0]
    L, U, piv = lu_decompose(A)
    x = lu_solve(L, U, piv, b)
    Ax = [sum(A[i][j]*x[j] for j in range(3)) for i in range(3)]
    assert all(abs(Ax[i]-b[i]) < 1e-8 for i in range(3))
    print("lu_decompose self-tests passed")
