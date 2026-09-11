"""Morphological operations – erode, dilate, open, close."""
from __future__ import annotations
from typing import List

Image = List[List[float]]


def erode(img: Image, size: int = 3) -> Image:
    h, w = len(img), len(img[0])
    r = size // 2
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            m = 1.0
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        m = min(m, img[ny][nx])
                    else:
                        m = 0.0
            out[y][x] = m
    return out


def dilate(img: Image, size: int = 3) -> Image:
    h, w = len(img), len(img[0])
    r = size // 2
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            m = 0.0
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        m = max(m, img[ny][nx])
            out[y][x] = m
    return out


def opening(img: Image, size: int = 3) -> Image:
    return dilate(erode(img, size), size)


def closing(img: Image, size: int = 3) -> Image:
    return erode(dilate(img, size), size)


if __name__ == "__main__":
    img = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    e = erode(img, 3)
    assert e[1][1] == 0.0
    d = dilate(img, 3)
    assert d[1][1] == 1.0
    print("morphology self-tests passed")
