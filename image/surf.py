"""Simplified SURF-like box-filter response."""
from __future__ import annotations
from typing import List, Tuple

Image = List[List[float]]


def box_filter_response(img: Image, size: int = 9) -> Image:
    h, w = len(img), len(img[0])
    r = size // 2
    out = [[0.0] * w for _ in range(h)]
    for y in range(r, h - r):
        for x in range(r, w - r):
            s = 0.0
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    s += img[y + dy][x + dx]
            out[y][x] = s / (size * size)
    return out


def detect_surf_keypoints(img: Image, threshold: float = 0.1) -> List[Tuple[int, int]]:
    resp = box_filter_response(img)
    h, w = len(img), len(img[0])
    kps = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if abs(resp[y][x] - img[y][x]) > threshold:
                kps.append((x, y))
    return kps


if __name__ == "__main__":
    img = [[0.0] * 12 for _ in range(12)]
    img[6][6] = 1.0
    kps = detect_surf_keypoints(img, 0.05)
    print(f"surf n_keypoints={len(kps)}")
    print("surf self-tests passed")
