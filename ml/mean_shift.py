"""
Universe Simulator - Mean Shift Clustering
Original kernel density mode seeking.
"""

from __future__ import annotations

import math
from typing import List, Tuple

def mean_shift(X: List[List[float]], bandwidth: float = 1.0, max_iter: int = 20) -> List[List[float]]:
    points = [p[:] for p in X]
    for _ in range(max_iter):
        new_points = []
        for p in points:
            num = [0.0] * len(p)
            den = 0.0
            for q in X:
                d2 = sum((a-b)**2 for a,b in zip(p, q))
                w = math.exp(-d2 / (2 * bandwidth ** 2))
                for i in range(len(p)):
                    num[i] += w * q[i]
                den += w
            if den > 1e-12:
                new_points.append([n / den for n in num])
            else:
                new_points.append(p)
        points = new_points
    return points

if __name__ == "__main__":
    X = [[0,0],[0.1,0.1],[0.2,0],[5,5],[5.1,5],[5.2,5.1]]
    modes = mean_shift(X, bandwidth=1.0)
    assert abs(modes[0][0] - modes[1][0]) < 1.0
    print("mean_shift self-test passed")
