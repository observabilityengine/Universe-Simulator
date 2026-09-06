"""Closest pair of points in 2D (divide and conquer).

Complexity: O(n log n).
Returns (distance, (p1, p2)). Assumes points are (x, y) tuples.
Original implementation.
"""
from __future__ import annotations

import math
from typing import List, Tuple

Point = Tuple[float, float]


def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def closest_pair(points: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    """Return minimum distance and the corresponding pair."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least 2 points")
    pts = sorted(set(points))  # unique, sorted by x then y
    if len(pts) < 2:
        raise ValueError("need at least 2 distinct points")

    def rec(px: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
        m = len(px)
        if m <= 3:
            best_d = float("inf")
            best_pair = (px[0], px[1])
            for i in range(m):
                for j in range(i + 1, m):
                    d = _dist(px[i], px[j])
                    if d < best_d:
                        best_d = d
                        best_pair = (px[i], px[j])
            return best_d, best_pair
        mid = m // 2
        mid_x = px[mid][0]
        dl, pair_l = rec(px[:mid])
        dr, pair_r = rec(px[mid:])
        d, pair = (dl, pair_l) if dl < dr else (dr, pair_r)
        strip = [p for p in px if abs(p[0] - mid_x) < d]
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= d:
                    break
                dj = _dist(strip[i], strip[j])
                if dj < d:
                    d = dj
                    pair = (strip[i], strip[j])
        return d, pair

    return rec(pts)


if __name__ == "__main__":
    pts = [(0, 0), (1, 1), (2, 2), (0.5, 0.1)]
    d, pair = closest_pair(pts)
    assert abs(d - _dist((0, 0), (0.5, 0.1))) < 1e-12
    d2, _ = closest_pair([(0, 0), (3, 4)])
    assert abs(d2 - 5.0) < 1e-12
    try:
        closest_pair([(1, 1)])
        assert False
    except ValueError:
        pass
    print("closest_pair self-tests passed")
