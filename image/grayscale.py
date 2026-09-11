"""RGB to grayscale conversion."""
from __future__ import annotations
from typing import List

Image = List[List[float]]
RGBImage = List[List[List[float]]]


def to_grayscale(img: RGBImage) -> Image:
    return [[0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] for p in row] for row in img]


def luminance(img: Image) -> float:
    h, w = len(img), len(img[0])
    return sum(sum(row) for row in img) / (h * w)


if __name__ == "__main__":
    rgb = [[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]]
    g = to_grayscale(rgb)
    assert len(g) == 2 and len(g[0]) == 2
    print(f"grayscale {g[0][0]:.1f}")
    print("grayscale self-tests passed")
