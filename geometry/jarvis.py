"""
Universe Simulator - Jarvis March (Gift Wrapping) Convex Hull
Original O(nh) implementation.
"""

from __future__ import annotations

from typing import List, Tuple

Point = Tuple[float, float]


def cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def jarvis_hull(points: List[Point]) -> List[Point]:
    if len(points) <= 2:
        return points[:]
    # leftmost
    start = min(points, key=lambda p: (p[0], p[1]))
    hull = []
    p = start
    while True:
        hull.append(p)
        q = points[0]
        for r in points[1:]:
            if q == p or cross(p, q, r) < 0:
                q = r
        p = q
        if p == start:
            break
    return hull


if __name__ == "__main__":
    pts = [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.2)]
    hull = jarvis_hull(pts)
    assert (0, 0) in hull and (2, 0) in hull
    print("jarvis self-test passed", hull)
