"""
Universe Simulator - Barnes-Hut force approximation (2-D demo)
Original quadtree-based gravity.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

Vec2 = Tuple[float, float]


@dataclass
class BHNode:
    cx: float
    cy: float
    size: float
    mass: float = 0.0
    com_x: float = 0.0
    com_y: float = 0.0
    body: Optional[Tuple[float, float, float]] = None  # x,y,m
    children: List[Optional["BHNode"]] = field(default_factory=lambda: [None] * 4)

    def insert(self, x: float, y: float, m: float) -> None:
        if self.mass == 0 and self.body is None:
            self.body = (x, y, m)
            self.mass = m
            self.com_x, self.com_y = x, y
            return
        if self.body is not None:
            ox, oy, om = self.body
            self.body = None
            self._quad_insert(ox, oy, om)
        self._quad_insert(x, y, m)
        # update COM
        total = self.mass + m
        self.com_x = (self.com_x * self.mass + x * m) / total
        self.com_y = (self.com_y * self.mass + y * m) / total
        self.mass = total

    def _quad_insert(self, x: float, y: float, m: float) -> None:
        hx = self.size * 0.5
        idx = (1 if x >= self.cx else 0) + (2 if y >= self.cy else 0)
        child = self.children[idx]
        if child is None:
            nx = self.cx - hx * 0.5 + (hx if x >= self.cx else 0)
            ny = self.cy - hx * 0.5 + (hx if y >= self.cy else 0)
            child = BHNode(nx, ny, hx)
            self.children[idx] = child
        child.insert(x, y, m)


def barnes_hut_forces(
    bodies: List[Tuple[float, float, float]],
    theta: float = 0.5,
    G: float = 1.0,
) -> List[Vec2]:
    if not bodies:
        return []
    xs = [b[0] for b in bodies]
    ys = [b[1] for b in bodies]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    size = max(maxx - minx, maxy - miny) + 1e-6
    root = BHNode((minx + maxx) * 0.5, (miny + maxy) * 0.5, size)
    for x, y, m in bodies:
        root.insert(x, y, m)

    forces = []
    for i, (x, y, m) in enumerate(bodies):
        fx = fy = 0.0

        def walk(node: BHNode) -> None:
            nonlocal fx, fy
            if node.mass == 0:
                return
            dx = node.com_x - x
            dy = node.com_y - y
            dist = math.sqrt(dx * dx + dy * dy) + 1e-9
            if node.body is not None or (node.size / dist < theta):
                if abs(dx) + abs(dy) > 1e-12:
                    f = G * m * node.mass / (dist * dist * dist)
                    fx += f * dx
                    fy += f * dy
                return
            for c in node.children:
                if c:
                    walk(c)

        walk(root)
        forces.append((fx, fy))
    return forces


if __name__ == "__main__":
    bodies = [(0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (0.5, 0.8, 1.0)]
    f = barnes_hut_forces(bodies)
    assert len(f) == 3
    print("barnes_hut self-test passed", f)
