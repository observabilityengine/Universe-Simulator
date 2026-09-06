"""Romberg integration (Richardson extrapolation of trapezoidal rule).

Complexity: O(2^max_levels) function evaluations.
Returns high-order approximation of ∫_a^b f(x) dx.
Original implementation.
"""
from __future__ import annotations

from typing import Callable
import numpy as np


def romberg(
    f: Callable[[float], float],
    a: float,
    b: float,
    max_levels: int = 6,
) -> float:
    """Romberg integration with max_levels Richardson levels."""
    if max_levels < 1:
        raise ValueError("max_levels >= 1")
    if a == b:
        return 0.0
    R = np.zeros((max_levels, max_levels))
    h = b - a
    R[0, 0] = 0.5 * h * (f(a) + f(b))
    for i in range(1, max_levels):
        h /= 2
        s = sum(f(a + (2 * k - 1) * h) for k in range(1, 2 ** (i - 1) + 1))
        R[i, 0] = 0.5 * R[i - 1, 0] + h * s
        for j in range(1, i + 1):
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / (4**j - 1)
    return float(R[max_levels - 1, max_levels - 1])


if __name__ == "__main__":
    est = romberg(lambda x: x * x, 0.0, 1.0, 6)
    assert abs(est - 1 / 3) < 1e-10
    import math
    est2 = romberg(math.sin, 0.0, math.pi, 8)
    assert abs(est2 - 2.0) < 1e-8
    assert romberg(lambda x: 1.0, 3.0, 3.0) == 0.0
    print("romberg self-tests passed")
