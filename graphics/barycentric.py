"""Barycentric coordinates for a point in a triangle."""
from __future__ import annotations
from typing import Tuple

Vec2 = Tuple[float, float]


def barycentric(v0: Vec2, v1: Vec2, v2: Vec2, p: Vec2) -> Tuple[float, float, float]:
    denom = (v1[1] - v2[1]) * (v0[0] - v2[0]) + (v2[0] - v1[0]) * (v0[1] - v2[1])
    if abs(denom) < 1e-12:
        return (-1.0, -1.0, -1.0)
    w0 = ((v1[1] - v2[1]) * (p[0] - v2[0]) + (v2[0] - v1[0]) * (p[1] - v2[1])) / denom
    w1 = ((v2[1] - v0[1]) * (p[0] - v2[0]) + (v0[0] - v2[0]) * (p[1] - v2[1])) / denom
    w2 = 1.0 - w0 - w1
    return (w0, w1, w2)


if __name__ == "__main__":
    w = barycentric((0, 0), (1, 0), (0, 1), (0.25, 0.25))
    assert abs(sum(w) - 1) < 1e-9
    assert all(x >= 0 for x in w)
    print(f"barycentric {w}")
    print("barycentric self-tests passed")
