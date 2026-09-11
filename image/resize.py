"""Bilinear image resize."""
from __future__ import annotations
from typing import List

Image = List[List[float]]


def resize(img: Image, new_h: int, new_w: int) -> Image:
    h, w = len(img), len(img[0])
    out = [[0.0] * new_w for _ in range(new_h)]
    for y in range(new_h):
        for x in range(new_w):
            sy = y * (h - 1) / max(new_h - 1, 1)
            sx = x * (w - 1) / max(new_w - 1, 1)
            y0, x0 = int(sy), int(sx)
            y1, x1 = min(y0 + 1, h - 1), min(x0 + 1, w - 1)
            fy, fx = sy - y0, sx - x0
            out[y][x] = (
                img[y0][x0] * (1 - fx) * (1 - fy)
                + img[y0][x1] * fx * (1 - fy)
                + img[y1][x0] * (1 - fx) * fy
                + img[y1][x1] * fx * fy
            )
    return out


if __name__ == "__main__":
    img = [[1.0, 0.0], [0.0, 1.0]]
    out = resize(img, 4, 4)
    assert len(out) == 4 and len(out[0]) == 4
    print("resize self-tests passed")
