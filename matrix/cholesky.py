"""
Universe Simulator - Cholesky Decomposition
Original LL^T decomposition for SPD matrices.
"""

from __future__ import annotations

import math
from typing import List


def cholesky(A: List[List[float]]) -> List[List[float]]:
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] - s
                if val <= 0:
                    raise ValueError("matrix not positive definite")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A[i][j] - s) / L[j][j]
    return L


if __name__ == "__main__":
    A = [[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]]
    L = cholesky(A)
    # reconstruct
    n = 3
    recon = [[sum(L[i][k]*L[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            assert abs(recon[i][j] - A[i][j]) < 1e-9
    print("cholesky self-test passed")
