"""
Module 78 – Convex Hull
Andrew's monotone chain algorithm.
Complete implementation.
"""

from __future__ import annotations
from typing import List, Tuple

Point = Tuple[float, float]


def cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: List[Point]) -> List[Point]:
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    print("Testing Convex Hull...")
    pts = [(0, 0), (1, 1), (2, 0), (1, 0.5), (0.5, 0.2), (1.5, 0.1), (3, 1), (2, 2)]
    hull = convex_hull(pts)
    print(f"  Input points: {len(pts)}")
    print(f"  Hull: {hull}")
    print(f"  Hull size: {len(hull)}")
    print("Convex Hull module OK.")
