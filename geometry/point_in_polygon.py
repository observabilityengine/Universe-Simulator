"""Point-in-polygon test via ray casting.

Complexity: O(n) for n-vertex polygon.
Returns True if point is strictly inside; boundary handling is inclusive on edges.
Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple

Point = Tuple[float, float]


def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    """Ray-casting PIP test. polygon is a list of vertices in order (closed implicitly)."""
    if len(polygon) < 3:
        return False
    x, y = point
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-30) + xi):
            inside = not inside
        j = i
    return inside


if __name__ == "__main__":
    square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    assert point_in_polygon((5, 5), square)
    assert not point_in_polygon((15, 5), square)
    assert not point_in_polygon((5, 5), [(0, 0), (1, 0)])  # not a polygon
    triangle = [(0, 0), (4, 0), (2, 3)]
    assert point_in_polygon((2, 1), triangle)
    assert not point_in_polygon((0, 3), triangle)
    print("point_in_polygon self-tests passed")
