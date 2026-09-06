"""Pearson correlation coefficient.

Complexity: O(n).
Returns r in [-1, 1]. Original implementation.
"""
from __future__ import annotations

import math
from typing import Sequence


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    """Pearson r for paired samples x, y."""
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("need equal-length sequences with n >= 2")
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = 0.0
    den_x = 0.0
    den_y = 0.0
    for xi, yi in zip(x, y):
        dx = xi - mean_x
        dy = yi - mean_y
        num += dx * dy
        den_x += dx * dx
        den_y += dy * dy
    den = math.sqrt(den_x * den_y)
    if den < 1e-15:
        return 0.0
    return num / den


if __name__ == "__main__":
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, 8.0, 10.0]
    assert abs(pearson(x, y) - 1.0) < 1e-12
    y2 = [10.0, 8.0, 6.0, 4.0, 2.0]
    assert abs(pearson(x, y2) - (-1.0)) < 1e-12
    try:
        pearson([1], [2])
        assert False
    except ValueError:
        pass
    print("pearson self-tests passed")
