"""Sobel edge detection."""
from __future__ import annotations
import math
from typing import List, Tuple

Image = List[List[float]]


def sobel(img: Image) -> Tuple[Image, Image, Image]:
    h, w = len(img), len(img[0])
    gx = [[0.0] * w for _ in range(h)]
    gy = [[0.0] * w for _ in range(h)]
    mag = [[0.0] * w for _ in range(h)]
    kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            sx = sy = 0.0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    v = img[y + dy][x + dx]
                    sx += v * kx[dy + 1][dx + 1]
                    sy += v * ky[dy + 1][dx + 1]
            gx[y][x] = sx
            gy[y][x] = sy
            mag[y][x] = math.sqrt(sx * sx + sy * sy)
    return gx, gy, mag


if __name__ == "__main__":
    img = [[0]*5 for _ in range(5)]
    for i in range(5):
        img[i][2] = 1.0
    _, _, mag = sobel(img)
    assert mag[2][1] > 0 or mag[2][3] > 0
    print(f"sobel max={max(max(r) for r in mag):.2f}")
    print("sobel self-tests passed")
