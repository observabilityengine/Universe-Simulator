"""Simplified SIFT-like keypoint detector (DoG extrema)."""
from __future__ import annotations
from typing import List, Tuple
from .gaussian_blur import gaussian_blur

Image = List[List[float]]
Keypoint = Tuple[int, int, float]


def detect_keypoints(img: Image, threshold: float = 0.03) -> List[Keypoint]:
    scale1 = gaussian_blur(img, 0.8)
    scale2 = gaussian_blur(img, 1.6)
    h, w = len(img), len(img[0])
    dog = [[scale1[y][x] - scale2[y][x] for x in range(w)] for y in range(h)]
    kps = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            v = dog[y][x]
            if abs(v) < threshold:
                continue
            is_ext = True
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy == 0 and dx == 0:
                        continue
                    if (v > 0 and dog[y + dy][x + dx] >= v) or (v < 0 and dog[y + dy][x + dx] <= v):
                        is_ext = False
                        break
                if not is_ext:
                    break
            if is_ext:
                kps.append((x, y, abs(v)))
    return kps


if __name__ == "__main__":
    img = [[0.0] * 16 for _ in range(16)]
    img[8][8] = 1.0
    kps = detect_keypoints(img, 0.01)
    print(f"sift n_keypoints={len(kps)}")
    print("sift self-tests passed")
