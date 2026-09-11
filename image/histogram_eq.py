"""Histogram equalization."""
from __future__ import annotations
from typing import List

Image = List[List[float]]


def histogram_equalize(img: Image) -> Image:
    flat = [v for row in img for v in row]
    n = len(flat)
    hist = [0] * 256
    for v in flat:
        hist[min(255, max(0, int(v * 255)))] += 1
    cdf = [0] * 256
    cdf[0] = hist[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + hist[i]
    cdf_min = next((c for c in cdf if c > 0), 0)
    h, w = len(img), len(img[0])
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            idx = min(255, max(0, int(img[y][x] * 255)))
            out[y][x] = (cdf[idx] - cdf_min) / max(n - cdf_min, 1)
    return out


if __name__ == "__main__":
    img = [[0.1, 0.1], [0.9, 0.9]]
    eq = histogram_equalize(img)
    assert eq[0][0] < eq[1][1]
    print("histogram_eq self-tests passed")
