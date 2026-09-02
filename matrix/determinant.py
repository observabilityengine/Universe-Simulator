"""
Universe Simulator - Matrix Determinant via LU
Original implementation.
"""

from __future__ import annotations

from typing import List


def determinant(A: List[List[float]]) -> float:
    n = len(A)
    M = [row[:] for row in A]
    det = 1.0
    for i in range(n):
        # partial pivot
        pivot = i
        for r in range(i+1, n):
            if abs(M[r][i]) > abs(M[pivot][i]):
                pivot = r
        if abs(M[pivot][i]) < 1e-12:
            return 0.0
        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
            det = -det
        det *= M[i][i]
        for r in range(i+1, n):
            factor = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] -= factor * M[i][c]
    return det


if __name__ == "__main__":
    A = [[1.0, 2.0, 3.0], [0.0, 1.0, 4.0], [5.0, 6.0, 0.0]]
    d = determinant(A)
    assert abs(d - 1.0) < 1e-9  # known det = 1
    print("determinant self-test passed", d)
