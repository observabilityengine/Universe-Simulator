"""Image rotation by 90 degree multiples and arbitrary angle."""
from __future__ import annotations
import math
from typing import List

Image = List[List[float]]


def rotate90(img: Image) -> Image:
    h, w = len(img), len(img[0])
    return [[img[h - 1 - r][c] for r in range(h)] for c in range(w)]


def rotate(img: Image, angle_deg: float) -> Image:
    h, w = len(img), len(img[0])
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    cx, cy = w / 2, h / 2
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            dx, dy = x - cx, y - cy
            sx = cos_a * dx + sin_a * dy + cx
            sy = -sin_a * dx + cos_a * dy + cy
            if 0 <= sx < w - 1 and 0 <= sy < h - 1:
                x0, y0 = int(sx), int(sy)
                fx, fy = sx - x0, sy - y0
                out[y][x] = (
                    img[y0][x0] * (1 - fx) * (1 - fy)
                    + img[y0][x0 + 1] * fx * (1 - fy)
                    + img[y0 + 1][x0] * (1 - fx) * fy
                    + img[y0 + 1][x0 + 1] * fx * fy
                )
    return out


if __name__ == "__main__":
    img = [[1, 2], [3, 4]]
    r = rotate90(img)
    assert r[0][0] == 3
    print("rotate self-tests passed")
