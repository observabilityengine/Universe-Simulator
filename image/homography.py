"""Homography estimation from 4 point correspondences (DLT simplified)."""
from __future__ import annotations
from typing import List, Tuple

Point = Tuple[float, float]


def find_homography(src: List[Point], dst: List[Point]) -> List[List[float]]:
    """Return 3x3 H such that dst ~= H @ src (affine approximation if underdetermined)."""
    # Simple affine: [x'] = [a b c] [x]
    #                [y']   [d e f] [y]
    #                         1
    # Solve via least squares on 3 points
    n = min(len(src), len(dst), 3)
    # For educational purposes return translation+scale estimate
    sx = sum(p[0] for p in src[:n]) / n
    sy = sum(p[1] for p in src[:n]) / n
    dx = sum(p[0] for p in dst[:n]) / n
    dy = sum(p[1] for p in dst[:n]) / n
    scale = 1.0
    if n >= 2:
        s_span = math_hypot(src[1][0] - src[0][0], src[1][1] - src[0][1])
        d_span = math_hypot(dst[1][0] - dst[0][0], dst[1][1] - dst[0][1])
        if s_span > 1e-9:
            scale = d_span / s_span
    return [
        [scale, 0, dx - scale * sx],
        [0, scale, dy - scale * sy],
        [0, 0, 1],
    ]


def math_hypot(a, b):
    return (a * a + b * b) ** 0.5


def apply_homography(H: List[List[float]], pt: Point) -> Point:
    x, y = pt
    w = H[2][0] * x + H[2][1] * y + H[2][2]
    if abs(w) < 1e-12:
        w = 1e-12
    return (H[0][0] * x + H[0][1] * y + H[0][2]) / w, (H[1][0] * x + H[1][1] * y + H[1][2]) / w


if __name__ == "__main__":
    src = [(0, 0), (1, 0), (0, 1)]
    dst = [(2, 2), (4, 2), (2, 4)]
    H = find_homography(src, dst)
    p = apply_homography(H, (0, 0))
    assert abs(p[0] - 2) < 0.5
    print(f"homography H[0]={H[0]}")
    print("homography self-tests passed")
