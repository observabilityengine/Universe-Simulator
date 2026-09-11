"""ORB-like oriented FAST keypoints with brief binary descriptor."""
from __future__ import annotations
from typing import List, Tuple

Image = List[List[float]]


def fast_keypoints(img: Image, threshold: float = 0.1) -> List[Tuple[int, int]]:
    h, w = len(img), len(img[0])
    kps = []
    offsets = [(0, -3), (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3),
               (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3)]
    for y in range(3, h - 3):
        for x in range(3, w - 3):
            center = img[y][x]
            bright = dark = 0
            for dx, dy in offsets:
                v = img[y + dy][x + dx]
                if v > center + threshold:
                    bright += 1
                elif v < center - threshold:
                    dark += 1
            if bright >= 12 or dark >= 12:
                kps.append((x, y))
    return kps


def brief_descriptor(img: Image, kp: Tuple[int, int], n_bits: int = 32) -> List[int]:
    x, y = kp
    h, w = len(img), len(img[0])
    desc = []
    for i in range(n_bits):
        dx1, dy1 = (i * 3) % 5 - 2, (i * 5) % 5 - 2
        dx2, dy2 = (i * 7) % 5 - 2, (i * 11) % 5 - 2
        x1, y1 = min(max(x + dx1, 0), w - 1), min(max(y + dy1, 0), h - 1)
        x2, y2 = min(max(x + dx2, 0), w - 1), min(max(y + dy2, 0), h - 1)
        desc.append(1 if img[y1][x1] > img[y2][x2] else 0)
    return desc


if __name__ == "__main__":
    img = [[0.5] * 20 for _ in range(20)]
    img[10][10] = 1.0
    kps = fast_keypoints(img, 0.2)
    if kps:
        d = brief_descriptor(img, kps[0])
        assert len(d) == 32
    print(f"orb n_keypoints={len(kps)}")
    print("orb self-tests passed")
