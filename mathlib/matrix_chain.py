"""Matrix chain ordering (dynamic programming).

Complexity: O(n^3) for n matrices.
Returns minimal multiplication cost and optimal parenthesization split.
"""
from __future__ import annotations

from typing import List, Tuple
import math


def matrix_chain_order(dims: List[int]) -> Tuple[int, List[List[int]]]:
    """Given dims of length n+1 for n matrices, return (min_cost, s) where s[i][j] is split.

    dims[i] x dims[i+1] is the shape of matrix i.
    """
    n = len(dims) - 1
    if n <= 0:
        return 0, []
    m = [[0] * n for _ in range(n)]
    s = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            m[i][j] = math.inf
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return int(m[0][n - 1]), s


if __name__ == "__main__":
    cost, _ = matrix_chain_order([10, 30, 5, 60])
    assert cost == 4500
    cost1, _ = matrix_chain_order([5, 10])
    assert cost1 == 0
    cost0, s0 = matrix_chain_order([1])
    assert cost0 == 0
    cost2, _ = matrix_chain_order([2, 2, 2, 2])
    assert cost2 == 16
    print("matrix_chain self-tests passed")
