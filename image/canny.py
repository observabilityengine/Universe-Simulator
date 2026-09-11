"""Canny edge detector (simplified)."""
from __future__ import annotations
from typing import List
from .gaussian_blur import gaussian_blur
from .sobel import sobel

Image = List[List[float]]


def non_max_suppression(mag: Image, gx: Image, gy: Image) -> Image:
    import math
    h, w = len(mag), len(mag[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            angle = math.atan2(gy[y][x], gx[y][x]) * 180 / math.pi
            angle = abs(angle)
            if angle < 22.5 or angle >= 157.5:
                n1, n2 = mag[y][x - 1], mag[y][x + 1]
            elif 22.5 <= angle < 67.5:
                n1, n2 = mag[y - 1][x + 1], mag[y + 1][x - 1]
            elif 67.5 <= angle < 112.5:
                n1, n2 = mag[y - 1][x], mag[y + 1][x]
            else:
                n1, n2 = mag[y - 1][x - 1], mag[y + 1][x + 1]
            if mag[y][x] >= n1 and mag[y][x] >= n2:
                out[y][x] = mag[y][x]
    return out


def canny(img: Image, low: float = 0.1, high: float = 0.3) -> Image:
    blurred = gaussian_blur(img, 1.0)
    gx, gy, mag = sobel(blurred)
    nms = non_max_suppression(mag, gx, gy)
    h, w = len(nms), len(nms[0])
    max_m = max(max(r) for r in nms) or 1.0
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            v = nms[y][x] / max_m
            if v >= high:
                out[y][x] = 1.0
            elif v >= low:
                out[y][x] = 0.5
    return out


if __name__ == "__main__":
    img = [[0.0]*8 for _ in range(8)]
    for i in range(8):
        img[i][4] = 1.0
    edges = canny(img)
    assert any(any(v > 0 for v in row) for row in edges)
    print("canny self-tests passed")
