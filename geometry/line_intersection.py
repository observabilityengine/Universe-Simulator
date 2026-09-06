"""2-D line segment intersection.

Complexity: O(1).
Returns intersection point or None if parallel / non-overlapping.
Original implementation using oriented cross products.
"""
from __future__ import annotations

from typing import Optional, Tuple

Point = Tuple[float, float]


def _cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def segment_intersection(
    p1: Point, p2: Point, p3: Point, p4: Point,
) -> Optional[Point]:
    """Return intersection of segments p1–p2 and p3–p4, or None."""
    d1 = _cross(p3, p4, p1)
    d2 = _cross(p3, p4, p2)
    d3 = _cross(p1, p2, p3)
    d4 = _cross(p1, p2, p4)
    if d1 * d2 > 0 or d3 * d4 > 0:
        return None  # same side → no proper intersection
    # parallel / collinear handling
    denom = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
    if abs(denom) < 1e-15:
        return None  # parallel or collinear (no unique point)
    t = ((p1[0] - p3[0]) * (p3[1] - p4[1]) - (p1[1] - p3[1]) * (p3[0] - p4[0])) / denom
    u = -((p1[0] - p2[0]) * (p1[1] - p3[1]) - (p1[1] - p2[1]) * (p1[0] - p3[0])) / denom
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
    return None


if __name__ == "__main__":
    pt = segment_intersection((0, 0), (2, 2), (0, 2), (2, 0))
    assert pt is not None and abs(pt[0] - 1) < 1e-10 and abs(pt[1] - 1) < 1e-10
    assert segment_intersection((0, 0), (1, 0), (0, 1), (1, 1)) is None
    assert segment_intersection((0, 0), (1, 1), (2, 2), (3, 3)) is None
    pt2 = segment_intersection((0, 0), (1, 0), (0.5, -1), (0.5, 1))
    assert pt2 is not None and abs(pt2[0] - 0.5) < 1e-10
    print("line_intersection self-tests passed")
