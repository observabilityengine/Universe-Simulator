"""2D KD-tree for geospatial nearest-neighbour."""
from __future__ import annotations
from typing import List, Optional, Tuple

Point = Tuple[float, float]


class KDNode:
    def __init__(self, point: Point, left=None, right=None, axis: int = 0):
        self.point = point
        self.left = left
        self.right = right
        self.axis = axis


def build_kdtree(points: List[Point], depth: int = 0) -> Optional[KDNode]:
    if not points:
        return None
    axis = depth % 2
    points = sorted(points, key=lambda p: p[axis])
    mid = len(points) // 2
    return KDNode(points[mid], build_kdtree(points[:mid], depth + 1), build_kdtree(points[mid + 1 :], depth + 1), axis)


def nearest(node: Optional[KDNode], target: Point, best: Optional[Point] = None, best_dist: float = float("inf")) -> Tuple[Optional[Point], float]:
    if node is None:
        return best, best_dist
    d = (node.point[0] - target[0]) ** 2 + (node.point[1] - target[1]) ** 2
    if d < best_dist:
        best, best_dist = node.point, d
    axis = node.axis
    diff = target[axis] - node.point[axis]
    near, far = (node.left, node.right) if diff < 0 else (node.right, node.left)
    best, best_dist = nearest(near, target, best, best_dist)
    if diff * diff < best_dist:
        best, best_dist = nearest(far, target, best, best_dist)
    return best, best_dist


if __name__ == "__main__":
    pts = [(0, 0), (1, 1), (2, 0), (3, 3)]
    tree = build_kdtree(pts)
    nn, d = nearest(tree, (1.1, 1.1))
    assert nn == (1, 1)
    print(f"kdtree_geo nn={nn}")
    print("kdtree_geo self-tests passed")
