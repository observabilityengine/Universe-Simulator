"""
Universe Simulator - 1-D Gaussian Kernel Density Estimate
Original KDE implementation.
"""

from __future__ import annotations

import math
from typing import List


def kde_gaussian(data: List[float], x: float, bandwidth: float) -> float:
    if bandwidth <= 0:
        raise ValueError("bandwidth must be > 0")
    n = len(data)
    if n == 0:
        return 0.0
    s = 0.0
    inv = 1.0 / (bandwidth * math.sqrt(2 * math.pi))
    for d in data:
        u = (x - d) / bandwidth
        s += math.exp(-0.5 * u * u)
    return inv * s / n

if __name__ == "__main__":
    data = [0.0, 0.1, -0.1, 0.05, 1.0, 1.1]
    dens0 = kde_gaussian(data, 0.0, 0.3)
    dens1 = kde_gaussian(data, 1.0, 0.3)
    dens5 = kde_gaussian(data, 5.0, 0.3)
    assert dens0 > dens5 and dens1 > dens5
    print("kernel_density self-test passed", dens0, dens1, dens5)
