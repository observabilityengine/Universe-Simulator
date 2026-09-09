"""Barnes-Hut octree (quadtree in 2D) gravity – O(N log N)."""
from __future__ import annotations
import math
from typing import List, Optional, Tuple

Vec = List[float]


class BHNode:
    def __init__(self, center: Vec, half_size: float, dim: int = 2):
        self.center = center
        self.half = half_size
        self.dim = dim
        self.mass = 0.0
        self.com: Optional[Vec] = None
        self.particle: Optional[Tuple[int, Vec, float]] = None
        self.children: List[Optional["BHNode"]] = [None] * (2 ** dim)

    def insert(self, idx: int, pos: Vec, mass: float) -> None:
        if self.mass == 0 and self.particle is None and all(c is None for c in self.children):
            self.particle = (idx, pos[:], mass)
            self.mass = mass
            self.com = pos[:]
            return
        if self.particle is not None:
            old = self.particle
            self.particle = None
            self._subdivide_insert(old[0], old[1], old[2])
        self._subdivide_insert(idx, pos, mass)
        total = self.mass + mass
        if self.com is None:
            self.com = pos[:]
            self.mass = mass
        else:
            self.com = [(self.com[d] * self.mass + pos[d] * mass) / total for d in range(self.dim)]
            self.mass = total

    def _subdivide_insert(self, idx: int, pos: Vec, mass: float) -> None:
        child_idx = 0
        for d in range(self.dim):
            if pos[d] >= self.center[d]:
                child_idx |= 1 << d
        if self.children[child_idx] is None:
            offset = [0.0] * self.dim
            for d in range(self.dim):
                offset[d] = self.half / 2 * (1 if (child_idx >> d) & 1 else -1)
            child_center = [self.center[d] + offset[d] for d in range(self.dim)]
            self.children[child_idx] = BHNode(child_center, self.half / 2, self.dim)
        self.children[child_idx].insert(idx, pos, mass)

    def force_on(self, pos: Vec, G: float, theta: float, softening: float, exclude_idx: int = -1) -> Vec:
        acc = [0.0] * self.dim
        if self.mass == 0:
            return acc
        if self.particle is not None:
            if self.particle[0] == exclude_idx:
                return acc
            rvec = [self.com[d] - pos[d] for d in range(self.dim)]
            r2 = sum(x * x for x in rvec) + softening * softening
            r = math.sqrt(r2)
            inv = G * self.mass / (r2 * r)
            return [rvec[d] * inv for d in range(self.dim)]
        rvec = [self.com[d] - pos[d] for d in range(self.dim)]
        r = math.sqrt(sum(x * x for x in rvec)) + 1e-30
        if self.half * 2 / r < theta:
            r2 = r * r + softening * softening
            inv = G * self.mass / (r2 * math.sqrt(r2))
            return [rvec[d] * inv for d in range(self.dim)]
        for ch in self.children:
            if ch is not None:
                f = ch.force_on(pos, G, theta, softening, exclude_idx)
                for d in range(self.dim):
                    acc[d] += f[d]
        return acc


def build_tree(positions: List[Vec], masses: List[float], dim: int = 2) -> BHNode:
    mins = [min(p[d] for p in positions) for d in range(dim)]
    maxs = [max(p[d] for p in positions) for d in range(dim)]
    center = [(mins[d] + maxs[d]) / 2 for d in range(dim)]
    half = max(maxs[d] - mins[d] for d in range(dim)) / 2 + 1e-6
    root = BHNode(center, half, dim)
    for i, (p, m) in enumerate(zip(positions, masses)):
        root.insert(i, p, m)
    return root


def barnes_hut_accelerations(positions: List[Vec], masses: List[float], G: float = 1.0, theta: float = 0.5, softening: float = 1e-4) -> List[Vec]:
    dim = len(positions[0])
    root = build_tree(positions, masses, dim)
    return [root.force_on(positions[i], G, theta, softening, exclude_idx=i) for i in range(len(positions))]


if __name__ == "__main__":
    pos = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    masses = [1.0, 1.0, 1.0, 1.0]
    acc = barnes_hut_accelerations(pos, masses, theta=0.5)
    assert len(acc) == 4
    assert acc[0][0] > 0 and acc[0][1] > 0
    print(f"barnes_hut acc0={acc[0]}")
    print("barnes_hut self-tests passed")
