"""
Universe Simulator - Rapidly-exploring Random Tree (RRT)
Original 2-D RRT for path planning in continuous space.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Tuple

Point = Tuple[float, float]


class RRT:
    def __init__(self, start: Point, goal: Point, bounds: Tuple[Point, Point], step: float = 0.5):
        self.start = start
        self.goal = goal
        self.bounds = bounds
        self.step = step
        self.nodes: List[Point] = [start]
        self.parent: List[int] = [-1]

    def _rand(self, rng: random.Random) -> Point:
        (xmin, ymin), (xmax, ymax) = self.bounds
        return (rng.uniform(xmin, xmax), rng.uniform(ymin, ymax))

    def _nearest(self, q: Point) -> int:
        best = 0
        best_d = float("inf")
        for i, p in enumerate(self.nodes):
            d = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
            if d < best_d:
                best_d = d
                best = i
        return best

    def _steer(self, from_p: Point, to_p: Point) -> Point:
        dx = to_p[0] - from_p[0]
        dy = to_p[1] - from_p[1]
        dist = math.sqrt(dx * dx + dy * dy) or 1e-9
        if dist <= self.step:
            return to_p
        return (from_p[0] + self.step * dx / dist, from_p[1] + self.step * dy / dist)

    def grow(self, iterations: int = 1000, seed: int = 0) -> Optional[List[Point]]:
        rng = random.Random(seed)
        for _ in range(iterations):
            q_rand = self._rand(rng) if rng.random() > 0.1 else self.goal
            idx = self._nearest(q_rand)
            q_new = self._steer(self.nodes[idx], q_rand)
            self.nodes.append(q_new)
            self.parent.append(idx)
            if (q_new[0] - self.goal[0]) ** 2 + (q_new[1] - self.goal[1]) ** 2 < self.step ** 2:
                # reconstruct
                path = [self.goal]
                i = len(self.nodes) - 1
                while i != -1:
                    path.append(self.nodes[i])
                    i = self.parent[i]
                path.reverse()
                return path
        return None


if __name__ == "__main__":
    rrt = RRT((0, 0), (5, 5), ((-1, -1), (6, 6)), step=0.8)
    path = rrt.grow(2000, seed=7)
    assert path is not None and path[0] == (0, 0)
    print("rrt self-test passed, path length", len(path))
