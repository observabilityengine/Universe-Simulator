"""Distance from point to line segment in 2D.

Complexity: O(1).
Original implementation.
"""
from __future__ import annotations

import math
from typing import Tuple

Point = Tuple[float, float]


def point_segment_distance(p: Point, a: Point, b: Point) -> float:
    """Minimum distance from point p to segment ab."""
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    len2 = dx * dx + dy * dy
    if len2 < 1e-30:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / len2))
    projx = ax + t * dx
    projy = ay + t * dy
    return math.hypot(px - projx, py - projy)


if __name__ == "__main__":
    assert abs(point_segment_distance((0, 1), (0, 0), (2, 0)) - 1.0) < 1e-12
    assert abs(point_segment_distance((3, 0), (0, 0), (2, 0)) - 1.0) < 1e-12
    assert abs(point_segment_distance((1, 0), (0, 0), (2, 0))) < 1e-12
    assert abs(point_segment_distance((0, 0), (0, 0), (0, 0))) < 1e-12
    print("segment_distance self-tests passed")
