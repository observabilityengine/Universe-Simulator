"""Kernel Density Estimation (Gaussian kernel).

Complexity: O(n * m) for m evaluation points. Original implementation.
"""
from __future__ import annotations
from typing import List
import math

def kde(
    data: List[float],
    eval_points: List[float],
    bandwidth: float | None = None,
) -> List[float]:
    n = len(data)
    if bandwidth is None:
        std = (sum((x - sum(data)/n)**2 for x in data)/n)**0.5
        bandwidth = 1.06 * std * n**(-0.2) if std > 0 else 1.0
    dens = []
    norm = 1.0 / (n * bandwidth * math.sqrt(2*math.pi))
    for x in eval_points:
        s = sum(math.exp(-0.5 * ((x - xi)/bandwidth)**2) for xi in data)
        dens.append(norm * s)
    return dens

if __name__ == "__main__":
    data = [0.0, 0.1, -0.1, 0.05, 1.0, 1.1, 0.9, 1.05]
    xs = [-1, 0, 0.5, 1, 2]
    d = kde(data, xs)
    assert d[1] > d[0]
    assert d[3] > d[4]
    print("kde self-tests passed")
