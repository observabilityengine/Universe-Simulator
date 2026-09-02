"""
Universe Simulator - Newtonian Gravity & Softened Potential
Original pairwise force and potential computation.
"""

from __future__ import annotations

import math
from typing import List, Tuple

Vec3 = Tuple[float, float, float]

G = 6.67430e-11


def pairwise_forces(
    positions: List[Vec3],
    masses: List[float],
    softening: float = 1e-4,
) -> List[Vec3]:
    n = len(positions)
    forces = [(0.0, 0.0, 0.0) for _ in range(n)]
    eps2 = softening * softening
    for i in range(n):
        fx = fy = fz = 0.0
        for j in range(n):
            if i == j:
                continue
            dx = positions[j][0] - positions[i][0]
            dy = positions[j][1] - positions[i][1]
            dz = positions[j][2] - positions[i][2]
            r2 = dx * dx + dy * dy + dz * dz + eps2
            r = math.sqrt(r2)
            f = G * masses[i] * masses[j] / (r2 * r)
            fx += f * dx
            fy += f * dy
            fz += f * dz
        forces[i] = (fx, fy, fz)
    return forces


def potential_energy(
    positions: List[Vec3],
    masses: List[float],
    softening: float = 1e-4,
) -> float:
    n = len(positions)
    pe = 0.0
    eps2 = softening * softening
    for i in range(n):
        for j in range(i + 1, n):
            dx = positions[j][0] - positions[i][0]
            dy = positions[j][1] - positions[i][1]
            dz = positions[j][2] - positions[i][2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz + eps2)
            pe -= G * masses[i] * masses[j] / r
    return pe


if __name__ == "__main__":
    pos = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
    m = [1.0, 1.0]
    f = pairwise_forces(pos, m, softening=0.01)
    pe = potential_energy(pos, m, softening=0.01)
    assert f[0][0] > 0 and f[1][0] < 0
    print("gravity self-test passed", f[0], pe)
