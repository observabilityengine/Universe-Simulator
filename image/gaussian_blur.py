"""Gaussian blur via separable convolution."""
from __future__ import annotations
import math
from typing import List

Image = List[List[float]]


def gaussian_kernel(sigma: float = 1.0, radius: int = 2) -> List[float]:
    k = [math.exp(-0.5 * (i / sigma) ** 2) for i in range(-radius, radius + 1)]
    s = sum(k)
    return [v / s for v in k]


def convolve1d(row: List[float], kernel: List[float]) -> List[float]:
    r = len(kernel) // 2
    n = len(row)
    out = []
    for i in range(n):
        acc = 0.0
        for j, kv in enumerate(kernel):
            idx = min(max(i + j - r, 0), n - 1)
            acc += row[idx] * kv
        out.append(acc)
    return out


def gaussian_blur(img: Image, sigma: float = 1.0) -> Image:
    k = gaussian_kernel(sigma)
    tmp = [convolve1d(row, k) for row in img]
    # transpose, blur, transpose
    cols = [[tmp[r][c] for r in range(len(tmp))] for c in range(len(tmp[0]))]
    blurred_cols = [convolve1d(col, k) for col in cols]
    return [[blurred_cols[c][r] for c in range(len(blurred_cols))] for r in range(len(blurred_cols[0]))]


if __name__ == "__main__":
    img = [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]
    out = gaussian_blur(img, 0.8)
    assert out[1][1] < 1.0 and out[1][1] > 0
    print(f"gaussian_blur center={out[1][1]:.3f}")
    print("gaussian_blur self-tests passed")
