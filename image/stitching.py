"""Simple panorama stitching via horizontal blend."""
from __future__ import annotations
from typing import List

Image = List[List[float]]


def stitch_horizontal(left: Image, right: Image, overlap: int = 10) -> Image:
    h = min(len(left), len(right))
    w_l, w_r = len(left[0]), len(right[0])
    out_w = w_l + w_r - overlap
    out = [[0.0] * out_w for _ in range(h)]
    for y in range(h):
        for x in range(w_l - overlap):
            out[y][x] = left[y][x]
        for x in range(overlap):
            alpha = x / max(overlap - 1, 1)
            out[y][w_l - overlap + x] = (1 - alpha) * left[y][w_l - overlap + x] + alpha * right[y][x]
        for x in range(overlap, w_r):
            out[y][w_l - overlap + x] = right[y][x]
    return out


if __name__ == "__main__":
    left = [[1.0] * 20 for _ in range(5)]
    right = [[0.0] * 20 for _ in range(5)]
    out = stitch_horizontal(left, right, 5)
    assert len(out[0]) == 35
    print(f"stitching width={len(out[0])}")
    print("stitching self-tests passed")
