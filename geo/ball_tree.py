"""Ball tree for range queries."""
from __future__ import annotations
from typing import List, Optional, Tuple
import math

Point = Tuple[float, float]


class BallNode:
    def __init__(self, center: Point, radius: float, points: List[Point] = None, left=None, right=None):
        self.center = center
        self.radius = radius
        self.points = points or []
        self.left = left
        self.right = right


def _dist(a: Point, b: Point) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def build_ball_tree(points: List[Point], leaf_size: int = 4) -> Optional[BallNode]:
    if not points:
        return None
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    center = (cx, cy)
    radius = max(_dist(center, p) for p in points)
    if len(points) <= leaf_size:
        return BallNode(center, radius, points)
    points = sorted(points, key=lambda p: p[0])
    mid = len(points) // 2
    return BallNode(center, radius, left=build_ball_tree(points[:mid], leaf_size), right=build_ball_tree(points[mid:], leaf_size))


def range_query(node: Optional[BallNode], target: Point, r: float) -> List[Point]:
    if node is None:
        return []
    if _dist(node.center, target) > node.radius + r:
        return []
    if node.points:
        return [p for p in node.points if _dist(p, target) <= r]
    return range_query(node.left, target, r) + range_query(node.right, target, r)


if __name__ == "__main__":
    pts = [(0, 0), (1, 0), (0, 1), (5, 5)]
    tree = build_ball_tree(pts)
    res = range_query(tree, (0, 0), 1.5)
    assert len(res) >= 2
    print(f"ball_tree range={res}")
    print("ball_tree self-tests passed")
