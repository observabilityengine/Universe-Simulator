"""
Universe Simulator - Ray-AABB and Ray-Sphere intersection
Original analytic tests.
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

Vec3 = Tuple[float, float, float]


def ray_sphere(
    origin: Vec3, direction: Vec3, center: Vec3, radius: float
) -> Optional[float]:
    """Return nearest positive t or None."""
    oc = (origin[0] - center[0], origin[1] - center[1], origin[2] - center[2])
    a = direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2
    b = 2 * (oc[0] * direction[0] + oc[1] * direction[1] + oc[2] * direction[2])
    c = oc[0] ** 2 + oc[1] ** 2 + oc[2] ** 2 - radius ** 2
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    sqrt_d = math.sqrt(disc)
    t0 = (-b - sqrt_d) / (2 * a)
    t1 = (-b + sqrt_d) / (2 * a)
    if t0 > 1e-9:
        return t0
    if t1 > 1e-9:
        return t1
    return None


def ray_aabb(
    origin: Vec3, direction: Vec3, amin: Vec3, amax: Vec3
) -> Optional[float]:
    tmin = 0.0
    tmax = float("inf")
    for i in range(3):
        if abs(direction[i]) < 1e-12:
            if origin[i] < amin[i] or origin[i] > amax[i]:
                return None
            continue
        inv = 1.0 / direction[i]
        t1 = (amin[i] - origin[i]) * inv
        t2 = (amax[i] - origin[i]) * inv
        if t1 > t2:
            t1, t2 = t2, t1
        tmin = max(tmin, t1)
        tmax = min(tmax, t2)
        if tmin > tmax:
            return None
    return tmin if tmin > 1e-9 else (tmax if tmax > 1e-9 else None)


if __name__ == "__main__":
    t = ray_sphere((0, 0, 0), (1, 0, 0), (5, 0, 0), 1.0)
    assert t is not None and abs(t - 4.0) < 1e-6
    t2 = ray_aabb((0, 0, 0), (1, 0, 0), (2, -1, -1), (4, 1, 1))
    assert t2 is not None and abs(t2 - 2.0) < 1e-6
    print("raycast self-test passed", t, t2)
