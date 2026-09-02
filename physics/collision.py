"""
Universe Simulator - Collision Detection & Response
Original sphere-sphere and AABB utilities + impulse response.
"""

from __future__ import annotations

import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def sphere_sphere(
    c1: Vec3, r1: float, c2: Vec3, r2: float
) -> bool:
    dx = c1[0] - c2[0]
    dy = c1[1] - c2[1]
    dz = c1[2] - c2[2]
    r = r1 + r2
    return dx * dx + dy * dy + dz * dz <= r * r


def aabb_overlap(
    min1: Vec3, max1: Vec3, min2: Vec3, max2: Vec3
) -> bool:
    return (
        min1[0] <= max2[0] and max1[0] >= min2[0]
        and min1[1] <= max2[1] and max1[1] >= min2[1]
        and min1[2] <= max2[2] and max1[2] >= min2[2]
    )


def resolve_sphere_impulse(
    p1: Vec3, v1: Vec3, m1: float,
    p2: Vec3, v2: Vec3, m2: float,
    restitution: float = 0.8,
) -> Tuple[Vec3, Vec3]:
    """Elastic/inelastic impulse for two spheres."""
    nx = p2[0] - p1[0]
    ny = p2[1] - p1[1]
    nz = p2[2] - p1[2]
    dist = math.sqrt(nx * nx + ny * ny + nz * nz) or 1e-9
    nx /= dist
    ny /= dist
    nz /= dist
    # relative velocity along normal
    rvx = v1[0] - v2[0]
    rvy = v1[1] - v2[1]
    rvz = v1[2] - v2[2]
    vel_along = rvx * nx + rvy * ny + rvz * nz
    if vel_along > 0:
        return v1, v2  # separating
    inv_m = 1.0 / m1 + 1.0 / m2
    j = -(1.0 + restitution) * vel_along / inv_m
    jx, jy, jz = j * nx, j * ny, j * nz
    new_v1 = (v1[0] - jx / m1, v1[1] - jy / m1, v1[2] - jz / m1)
    new_v2 = (v2[0] + jx / m2, v2[1] + jy / m2, v2[2] + jz / m2)
    return new_v1, new_v2


if __name__ == "__main__":
    assert sphere_sphere((0, 0, 0), 1.0, (1.5, 0, 0), 1.0)
    assert not sphere_sphere((0, 0, 0), 1.0, (3.0, 0, 0), 1.0)
    v1, v2 = resolve_sphere_impulse(
        (0, 0, 0), (1, 0, 0), 1.0,
        (2, 0, 0), (-1, 0, 0), 1.0,
        restitution=1.0,
    )
    print("collision self-test passed", v1, v2)
