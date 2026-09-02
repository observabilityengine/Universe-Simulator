"""
Universe Simulator - Axis-Aligned Bounding Box utilities
Original AABB construction, merge, intersection, volume.
"""

from __future__ import annotations

from typing import Tuple, Iterable

Vec3 = Tuple[float, float, float]
AABB = Tuple[Vec3, Vec3]  # (min, max)


def make_aabb(points: Iterable[Vec3]) -> AABB:
    pts = list(points)
    if not pts:
        raise ValueError("empty point set")
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    zs = [p[2] for p in pts]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def merge(a: AABB, b: AABB) -> AABB:
    return (
        (min(a[0][0], b[0][0]), min(a[0][1], b[0][1]), min(a[0][2], b[0][2])),
        (max(a[1][0], b[1][0]), max(a[1][1], b[1][1]), max(a[1][2], b[1][2])),
    )


def intersects(a: AABB, b: AABB) -> bool:
    return (
        a[0][0] <= b[1][0] and a[1][0] >= b[0][0]
        and a[0][1] <= b[1][1] and a[1][1] >= b[0][1]
        and a[0][2] <= b[1][2] and a[1][2] >= b[0][2]
    )


def volume(a: AABB) -> float:
    return max(0.0, a[1][0] - a[0][0]) * max(0.0, a[1][1] - a[0][1]) * max(0.0, a[1][2] - a[0][2])


if __name__ == "__main__":
    box = make_aabb([(0, 0, 0), (1, 2, 3), (-1, 0.5, 0)])
    assert box[0] == (-1, 0, 0) and box[1] == (1, 2, 3)
    assert volume(box) == 2 * 2 * 3
    print("aabb self-test passed")
