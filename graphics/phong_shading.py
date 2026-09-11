"""Classic Phong reflection model."""
from __future__ import annotations
import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(a: Vec3) -> Vec3:
    l = math.sqrt(_dot(a, a)) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


def _reflect(i: Vec3, n: Vec3) -> Vec3:
    d = 2 * _dot(i, n)
    return (d * n[0] - i[0], d * n[1] - i[1], d * n[2] - i[2])


def phong(
    normal: Vec3,
    view: Vec3,
    light_dir: Vec3,
    kd: Vec3 = (0.7, 0.7, 0.7),
    ks: Vec3 = (1.0, 1.0, 1.0),
    shininess: float = 32.0,
    ka: float = 0.1,
) -> Vec3:
    n = _norm(normal)
    v = _norm(view)
    l = _norm(light_dir)
    ndotl = max(0.0, _dot(n, l))
    r = _reflect(l, n)
    rdotv = max(0.0, _dot(r, v))
    spec = rdotv ** shininess
    return (
        ka * kd[0] + ndotl * kd[0] + spec * ks[0],
        ka * kd[1] + ndotl * kd[1] + spec * ks[1],
        ka * kd[2] + ndotl * kd[2] + spec * ks[2],
    )


if __name__ == "__main__":
    c = phong((0, 0, 1), (0, 0, 1), (0, 0, 1))
    assert c[0] > 0.5
    print(f"phong_shading {c}")
    print("phong_shading self-tests passed")
