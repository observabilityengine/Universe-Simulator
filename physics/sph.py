"""
Universe Simulator - Minimal SPH density estimator
Original smoothed-particle hydrodynamics density kernel (poly6).
"""

from __future__ import annotations

import math
from typing import List, Tuple

Vec3 = Tuple[float, float, float]


def poly6(r: float, h: float) -> float:
    if r >= h or r < 0:
        return 0.0
    factor = 315.0 / (64.0 * math.pi * h ** 9)
    return factor * (h * h - r * r) ** 3


def density(
    positions: List[Vec3],
    masses: List[float],
    h: float,
) -> List[float]:
    n = len(positions)
    rho = [0.0] * n
    for i in range(n):
        for j in range(n):
            dx = positions[i][0] - positions[j][0]
            dy = positions[i][1] - positions[j][1]
            dz = positions[i][2] - positions[j][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz)
            rho[i] += masses[j] * poly6(r, h)
    return rho


if __name__ == "__main__":
    pos = [(0.0, 0.0, 0.0), (0.1, 0.0, 0.0), (0.0, 0.1, 0.0)]
    m = [1.0, 1.0, 1.0]
    rho = density(pos, m, h=0.5)
    assert all(r > 0 for r in rho)
    print("sph self-test passed", rho)
