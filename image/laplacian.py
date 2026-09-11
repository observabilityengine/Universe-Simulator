"""Laplacian edge filter."""
from __future__ import annotations
from typing import List

Image = List[List[float]]

KERNEL = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]


def laplacian(img: Image) -> Image:
    h, w = len(img), len(img[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            s = 0.0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    s += img[y + dy][x + dx] * KERNEL[dy + 1][dx + 1]
            out[y][x] = s
    return out


if __name__ == "__main__":
    img = [[0]*5 for _ in range(5)]
    img[2][2] = 1.0
    out = laplacian(img)
    assert out[2][2] < 0
    print("laplacian self-tests passed")
