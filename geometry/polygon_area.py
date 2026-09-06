"""Polygon area via shoelace formula.

Complexity: O(n).
Vertices in order (CW or CCW). Returns absolute area. Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple

Point = Tuple[float, float]


def polygon_area(vertices: List[Point]) -> float:
    """Shoelace area of simple polygon."""
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2.0


if __name__ == "__main__":
    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert abs(polygon_area(square) - 4.0) < 1e-12
    triangle = [(0, 0), (4, 0), (0, 3)]
    assert abs(polygon_area(triangle) - 6.0) < 1e-12
    assert polygon_area([(0, 0), (1, 0)]) == 0.0
    print("polygon_area self-tests passed")
