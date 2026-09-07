"""Matrix determinant via LU with partial pivoting.

Complexity: O(n^3). Original implementation.
"""
from __future__ import annotations

from typing import List


def determinant(A: List[List[float]]) -> float:
    n = len(A)
    M = [row[:] for row in A]
    det = 1.0
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[piv][k]) < 1e-15:
            return 0.0
        if piv != k:
            M[k], M[piv] = M[piv], M[k]
            det = -det
        det *= M[k][k]
        for i in range(k + 1, n):
            fac = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= fac * M[k][j]
    return det


if __name__ == "__main__":
    assert abs(determinant([[1, 2], [3, 4]]) - (-2)) < 1e-10
    assert abs(determinant([[2, 0, 0], [0, 3, 0], [0, 0, 4]]) - 24) < 1e-10
    assert abs(determinant([[1, 1], [1, 1]])) < 1e-10
    print("determinant self-tests passed")
