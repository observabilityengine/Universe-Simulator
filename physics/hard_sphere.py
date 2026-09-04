"""
Universe Simulator - Hard Sphere Collision Response
Original instantaneous collision for equal mass spheres.
"""

from __future__ import annotations

import math
from typing import Tuple

Vec3 = Tuple[float, float, float]

def hard_sphere_collision(
    p1: Vec3, v1: Vec3,
    p2: Vec3, v2: Vec3,
    r1: float, r2: float,
) -> Tuple[Vec3, Vec3]:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz) or 1e-9
    if dist > r1 + r2:
        return v1, v2
    nx, ny, nz = dx/dist, dy/dist, dz/dist
    dvx = v1[0] - v2[0]
    dvy = v1[1] - v2[1]
    dvz = v1[2] - v2[2]
    vn = dvx*nx + dvy*ny + dvz*nz
    if vn > 0:
        return v1, v2
    v1n = (v1[0] - vn*nx, v1[1] - vn*ny, v1[2] - vn*nz)
    v2n = (v2[0] + vn*nx, v2[1] + vn*ny, v2[2] + vn*nz)
    return v1n, v2n

if __name__ == "__main__":
    v1, v2 = hard_sphere_collision((0,0,0), (1,0,0), (1.5,0,0), (-1,0,0), 1.0, 1.0)
    assert v1[0] < 0 and v2[0] > 0
    print("hard_sphere self-test passed", v1, v2)
