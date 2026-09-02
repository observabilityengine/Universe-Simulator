"""
Universe Simulator - KD-Tree
Original pure-Python 3-D KD-tree for nearest-neighbour and range queries.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

Point = Tuple[float, float, float]


@dataclass
class KDNode:
    point: Point
    entity_id: str
    axis: int
    left: Optional["KDNode"] = None
    right: Optional["KDNode"] = None


class KDTree:
    def __init__(self, points: List[Tuple[str, Point]]):
        self.root = self._build(points, 0)

    def _build(self, pts: List[Tuple[str, Point]], depth: int) -> Optional[KDNode]:
        if not pts:
            return None
        axis = depth % 3
        pts.sort(key=lambda t: t[1][axis])
        mid = len(pts) // 2
        eid, p = pts[mid]
        node = KDNode(point=p, entity_id=eid, axis=axis)
        node.left = self._build(pts[:mid], depth + 1)
        node.right = self._build(pts[mid + 1:], depth + 1)
        return node

    def nearest(self, target: Point) -> Optional[Tuple[str, float]]:
        best: Optional[Tuple[str, float]] = None

        def _search(node: Optional[KDNode]) -> None:
            nonlocal best
            if node is None:
                return
            d2 = sum((a - b) ** 2 for a, b in zip(node.point, target))
            if best is None or d2 < best[1]:
                best = (node.entity_id, d2)
            axis = node.axis
            diff = target[axis] - node.point[axis]
            near, far = (node.left, node.right) if diff < 0 else (node.right, node.left)
            _search(near)
            if best is None or diff * diff < best[1]:
                _search(far)

        _search(self.root)
        if best is None:
            return None
        return best[0], math.sqrt(best[1])


if __name__ == "__main__":
    data = [
        ("p1", (0.0, 0.0, 0.0)),
        ("p2", (1.0, 0.0, 0.0)),
        ("p3", (0.0, 1.0, 0.0)),
        ("p4", (5.0, 5.0, 5.0)),
    ]
    tree = KDTree(data)
    eid, dist = tree.nearest((0.1, 0.1, 0.0))
    assert eid == "p1"
    print("kd_tree self-test passed", eid, dist)
