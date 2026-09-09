"""Quadtree for 2D spatial indexing."""
from __future__ import annotations
from typing import List, Tuple

Point = Tuple[float, float]
BBox = Tuple[float, float, float, float]


class QuadNode:
    def __init__(self, bbox: BBox, capacity: int = 4):
        self.bbox = bbox
        self.capacity = capacity
        self.points: List[Point] = []
        self.children: List["QuadNode"] = []

    def contains(self, p: Point) -> bool:
        x0, y0, x1, y1 = self.bbox
        return x0 <= p[0] < x1 and y0 <= p[1] < y1

    def subdivide(self):
        x0, y0, x1, y1 = self.bbox
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        self.children = [
            QuadNode((x0, y0, mx, my), self.capacity),
            QuadNode((mx, y0, x1, my), self.capacity),
            QuadNode((x0, my, mx, y1), self.capacity),
            QuadNode((mx, my, x1, y1), self.capacity),
        ]

    def insert(self, p: Point) -> bool:
        if not self.contains(p):
            return False
        if not self.children and len(self.points) < self.capacity:
            self.points.append(p)
            return True
        if not self.children:
            self.subdivide()
            for q in self.points:
                for c in self.children:
                    if c.insert(q):
                        break
            self.points.clear()
        for c in self.children:
            if c.insert(p):
                return True
        return False

    def query_range(self, bbox: BBox) -> List[Point]:
        x0, y0, x1, y1 = bbox
        bx0, by0, bx1, by1 = self.bbox
        if x1 < bx0 or bx1 < x0 or y1 < by0 or by1 < y0:
            return []
        result = [p for p in self.points if x0 <= p[0] <= x1 and y0 <= p[1] <= y1]
        for c in self.children:
            result.extend(c.query_range(bbox))
        return result


if __name__ == "__main__":
    root = QuadNode((0, 0, 10, 10))
    for p in [(1, 1), (2, 2), (8, 8), (9, 1)]:
        root.insert(p)
    res = root.query_range((0, 0, 3, 3))
    assert len(res) >= 2
    print(f"quadtree_geo {res}")
    print("quadtree_geo self-tests passed")
