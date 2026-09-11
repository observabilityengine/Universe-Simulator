"""Planar and spherical UV mapping."""
from __future__ import annotations
import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def planar_uv(p: Vec3, axis: str = "z") -> Tuple[float, float]:
    if axis == "z":
        return (p[0] * 0.5 + 0.5, p[1] * 0.5 + 0.5)
    if axis == "y":
        return (p[0] * 0.5 + 0.5, p[2] * 0.5 + 0.5)
    return (p[1] * 0.5 + 0.5, p[2] * 0.5 + 0.5)


def spherical_uv(p: Vec3) -> Tuple[float, float]:
    l = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2) or 1.0
    x, y, z = p[0]/l, p[1]/l, p[2]/l
    u = 0.5 + math.atan2(z, x) / (2 * math.pi)
    v = 0.5 - math.asin(max(-1, min(1, y))) / math.pi
    return (u, v)


if __name__ == "__main__":
    u, v = planar_uv((0, 0, 0))
    assert abs(u - 0.5) < 1e-9
    su, sv = spherical_uv((1, 0, 0))
    print(f"uv_mapping planar=({u},{v}) spherical=({su:.2f},{sv:.2f})")
    print("uv_mapping self-tests passed")
