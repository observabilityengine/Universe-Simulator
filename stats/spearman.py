"""Spearman rank correlation.

Complexity: O(n log n) due to ranking.
Returns ρ in [-1, 1]. Average ranks for ties. Original implementation.
"""
from __future__ import annotations

from typing import List, Sequence
from .pearson import pearson


def _rank(data: Sequence[float]) -> List[float]:
    n = len(data)
    indexed = sorted(range(n), key=lambda i: data[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and data[indexed[j + 1]] == data[indexed[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0  # 1-based average rank
        for k in range(i, j + 1):
            ranks[indexed[k]] = avg
        i = j + 1
    return ranks


def spearman(x: Sequence[float], y: Sequence[float]) -> float:
    """Spearman rank correlation of x and y."""
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("need equal-length sequences with n >= 2")
    return pearson(_rank(x), _rank(y))


if __name__ == "__main__":
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [5.0, 6.0, 7.0, 8.0, 7.0]
    r = spearman(x, y)
    assert -1.0 <= r <= 1.0
    assert abs(spearman(x, x) - 1.0) < 1e-12
    assert abs(spearman(x, list(reversed(x))) - (-1.0)) < 1e-12
    print("spearman self-tests passed")
