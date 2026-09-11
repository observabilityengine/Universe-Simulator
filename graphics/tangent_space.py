"""Tangent/bitangent computation for normal mapping."""
from __future__ import annotations
import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _norm(a: Vec3) -> Vec3:
    l = math.sqrt(a[0]**2+a[1]**2+a[2]**2) or 1.0
    return (a[0]/l, a[1]/l, a[2]/l)


def compute_tangent(p0: Vec3, p1: Vec3, p2: Vec3, uv0: Tuple[float,float], uv1: Tuple[float,float], uv2: Tuple[float,float]) -> Tuple[Vec3, Vec3]:
    e1 = (p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2])
    e2 = (p2[0]-p0[0], p2[1]-p0[1], p2[2]-p0[2])
    du1, dv1 = uv1[0]-uv0[0], uv1[1]-uv0[1]
    du2, dv2 = uv2[0]-uv0[0], uv2[1]-uv0[1]
    f = 1.0 / (du1 * dv2 - du2 * dv1 + 1e-12)
    t = _norm((f*(dv2*e1[0]-dv1*e2[0]), f*(dv2*e1[1]-dv1*e2[1]), f*(dv2*e1[2]-dv1*e2[2])))
    b = _norm((f*(-du2*e1[0]+du1*e2[0]), f*(-du2*e1[1]+du1*e2[1]), f*(-du2*e1[2]+du1*e2[2])))
    return t, b


if __name__ == "__main__":
    t, b = compute_tangent((0,0,0),(1,0,0),(0,1,0),(0,0),(1,0),(0,1))
    assert abs(t[0]) > 0.5
    print(f"tangent_space T={t} B={b}")
    print("tangent_space self-tests passed")
