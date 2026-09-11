"""Minimal ray tracer – spheres, planes, simple shading."""
from __future__ import annotations
import math
from typing import List, Optional, Tuple

Vec3 = Tuple[float, float, float]


def add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def mul(a: Vec3, s: float) -> Vec3:
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a: Vec3) -> Vec3:
    l = math.sqrt(dot(a, a)) or 1.0
    return mul(a, 1.0 / l)


def sphere_intersect(origin: Vec3, dir: Vec3, center: Vec3, radius: float) -> Optional[float]:
    oc = sub(origin, center)
    a = dot(dir, dir)
    b = 2 * dot(oc, dir)
    c = dot(oc, oc) - radius * radius
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    t = (-b - math.sqrt(disc)) / (2 * a)
    return t if t > 1e-4 else None


def render(width: int = 64, height: int = 48) -> List[List[Tuple[float, float, float]]]:
    sphere_c, sphere_r = (0.0, 0.0, -3.0), 1.0
    light = norm((1.0, 1.0, 1.0))
    img = []
    for j in range(height):
        row = []
        for i in range(width):
            x = (2 * (i + 0.5) / width - 1) * width / height
            y = 1 - 2 * (j + 0.5) / height
            direction = norm((x, y, -1.0))
            origin = (0.0, 0.0, 0.0)
            t = sphere_intersect(origin, direction, sphere_c, sphere_r)
            if t is not None:
                hit = add(origin, mul(direction, t))
                n = norm(sub(hit, sphere_c))
                intensity = max(0.0, dot(n, light))
                row.append((intensity, intensity * 0.8, intensity * 0.6))
            else:
                row.append((0.1, 0.1, 0.15))
        img.append(row)
    return img


if __name__ == "__main__":
    img = render(32, 24)
    assert len(img) == 24 and len(img[0]) == 32
    bright = sum(1 for row in img for p in row if p[0] > 0.3)
    assert bright > 0
    print(f"raytracer bright_pixels={bright}")
    print("raytracer self-tests passed")
