"""Axis-aligned bounding box (AABB) utilities in 2D.

Complexity: O(n) to compute from points; O(1) intersection/union.
Original implementation.
"""
from __future__ import annotations

from typing import List, Optional, Tuple

Point = Tuple[float, float]
AABB = Tuple[float, float, float, float]  # min_x, min_y, max_x, max_y


def aabb_from_points(points: List[Point]) -> AABB:
    if not points:
        raise ValueError("empty point set")
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (min(xs), min(ys), max(xs), max(ys))


def aabb_intersects(a: AABB, b: AABB) -> bool:
    return a[0] <= b[2] and a[2] >= b[0] and a[1] <= b[3] and a[3] >= b[1]


def aabb_union(a: AABB, b: AABB) -> AABB:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def aabb_intersection(a: AABB, b: AABB) -> Optional[AABB]:
    if not aabb_intersects(a, b):
        return None
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def aabb_contains_point(box: AABB, p: Point) -> bool:
    return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]


if __name__ == "__main__":
    box = aabb_from_points([(0, 0), (2, 3), (1, 1)])
    assert box == (0, 0, 2, 3)
    assert aabb_intersects((0, 0, 2, 2), (1, 1, 3, 3))
    assert not aabb_intersects((0, 0, 1, 1), (2, 2, 3, 3))
    assert aabb_union((0, 0, 1, 1), (2, 2, 3, 3)) == (0, 0, 3, 3)
    assert aabb_contains_point((0, 0, 2, 2), (1, 1))
    assert aabb_intersection((0, 0, 2, 2), (1, 1, 3, 3)) == (1, 1, 2, 2)
    print("bounding_box self-tests passed")
