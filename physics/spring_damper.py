"""
Universe Simulator - Spring-Damper Force
Original Hookean spring with viscous damping.
"""

from __future__ import annotations

import math
from typing import Tuple

Vec3 = Tuple[float, float, float]

def spring_damper_force(
    p1: Vec3, v1: Vec3,
    p2: Vec3, v2: Vec3,
    rest_length: float,
    stiffness: float,
    damping: float,
) -> Tuple[Vec3, Vec3]:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz) or 1e-9
    nx, ny, nz = dx/dist, dy/dist, dz/dist
    # relative velocity along spring
    dvx = v2[0] - v1[0]
    dvy = v2[1] - v1[1]
    dvz = v2[2] - v1[2]
    vrel = dvx*nx + dvy*ny + dvz*nz
    force_mag = stiffness * (dist - rest_length) + damping * vrel
    fx, fy, fz = force_mag * nx, force_mag * ny, force_mag * nz
    return (-fx, -fy, -fz), (fx, fy, fz)

if __name__ == "__main__":
    f1, f2 = spring_damper_force((0,0,0), (0,0,0), (2,0,0), (0,0,0), 1.0, 10.0, 0.5)
    assert f1[0] < 0 and f2[0] > 0
    print("spring_damper self-test passed", f1)
