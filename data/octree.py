"""
Universe Simulator - Octree Spatial Partition
Original pure-Python adaptive octree for 3-D point sets.
Supports insert, radius query, and recursive subdivision.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

Position3D = Tuple[float, float, float]


@dataclass
class OctreeNode:
    center: Position3D
    half_size: float
    points: List[Tuple[str, Position3D]] = field(default_factory=list)
    children: Optional[List["OctreeNode"]] = None
    max_points: int = 8
    max_depth: int = 12
    depth: int = 0

    def contains(self, pos: Position3D) -> bool:
        hs = self.half_size
        return (
            abs(pos[0] - self.center[0]) <= hs
            and abs(pos[1] - self.center[1]) <= hs
            and abs(pos[2] - self.center[2]) <= hs
        )

    def _subdivide(self) -> None:
        if self.children is not None:
            return
        hs = self.half_size * 0.5
        cx, cy, cz = self.center
        offsets = [
            (-hs, -hs, -hs), (hs, -hs, -hs), (-hs, hs, -hs), (hs, hs, -hs),
            (-hs, -hs, hs), (hs, -hs, hs), (-hs, hs, hs), (hs, hs, hs),
        ]
        self.children = []
        for ox, oy, oz in offsets:
            child = OctreeNode(
                center=(cx + ox, cy + oy, cz + oz),
                half_size=hs,
                max_points=self.max_points,
                max_depth=self.max_depth,
                depth=self.depth + 1,
            )
            self.children.append(child)
        # redistribute
        for eid, pos in self.points:
            for child in self.children:
                if child.contains(pos):
                    child.points.append((eid, pos))
                    break
        self.points.clear()

    def insert(self, entity_id: str, pos: Position3D) -> bool:
        if not self.contains(pos):
            return False
        if self.children is None:
            self.points.append((entity_id, pos))
            if len(self.points) > self.max_points and self.depth < self.max_depth:
                self._subdivide()
            return True
        for child in self.children:
            if child.insert(entity_id, pos):
                return True
        return False

    def query_radius(self, center: Position3D, radius: float, out: List[str]) -> None:
        # AABB vs sphere broad phase
        dx = abs(center[0] - self.center[0])
        dy = abs(center[1] - self.center[1])
        dz = abs(center[2] - self.center[2])
        if dx > self.half_size + radius or dy > self.half_size + radius or dz > self.half_size + radius:
            return
        if self.children is None:
            r2 = radius * radius
            for eid, p in self.points:
                d2 = (p[0]-center[0])**2 + (p[1]-center[1])**2 + (p[2]-center[2])**2
                if d2 <= r2:
                    out.append(eid)
            return
        for child in self.children:
            child.query_radius(center, radius, out)


class Octree:
    def __init__(self, center: Position3D = (0.0, 0.0, 0.0), half_size: float = 1000.0):
        self.root = OctreeNode(center=center, half_size=half_size)

    def insert(self, entity_id: str, pos: Position3D) -> bool:
        return self.root.insert(entity_id, pos)

    def query_radius(self, center: Position3D, radius: float) -> List[str]:
        out: List[str] = []
        self.root.query_radius(center, radius, out)
        return out


if __name__ == "__main__":
    ot = Octree(half_size=100.0)
    ot.insert("a", (1.0, 2.0, 3.0))
    ot.insert("b", (1.5, 2.1, 3.2))
    ot.insert("c", (50.0, 50.0, 50.0))
    hits = ot.query_radius((1.0, 2.0, 3.0), 2.0)
    assert "a" in hits and "b" in hits and "c" not in hits
    print("octree self-test passed", hits)
