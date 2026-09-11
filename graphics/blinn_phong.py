"""Blinn-Phong shading model."""
from __future__ import annotations
import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(a: Vec3) -> Vec3:
    l = math.sqrt(_dot(a, a)) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


def _add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def blinn_phong(
    normal: Vec3,
    view: Vec3,
    light: Vec3,
    diffuse_color: Vec3 = (0.8, 0.8, 0.8),
    specular_color: Vec3 = (1.0, 1.0, 1.0),
    shininess: float = 32.0,
    ambient: float = 0.1,
) -> Vec3:
    n = _norm(normal)
    v = _norm(view)
    l = _norm(light)
    ndotl = max(0.0, _dot(n, l))
    half = _norm(_add(l, v))
    ndoth = max(0.0, _dot(n, half))
    spec = ndoth ** shininess
    return (
        ambient * diffuse_color[0] + ndotl * diffuse_color[0] + spec * specular_color[0],
        ambient * diffuse_color[1] + ndotl * diffuse_color[1] + spec * specular_color[1],
        ambient * diffuse_color[2] + ndotl * diffuse_color[2] + spec * specular_color[2],
    )


if __name__ == "__main__":
    c = blinn_phong((0, 0, 1), (0, 0, 1), (0, 0, 1))
    assert c[0] > 0.5
    print(f"blinn_phong {c}")
    print("blinn_phong self-tests passed")
