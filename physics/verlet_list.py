"""
Universe Simulator - Verlet Neighbor List
Original skin-radius neighbor list for molecular dynamics.
"""

from __future__ import annotations

import math
from typing import List, Tuple

Vec3 = Tuple[float, float, float]


class VerletList:
    def __init__(self, cutoff: float, skin: float):
        self.cutoff = cutoff
        self.skin = skin
        self.r_list = cutoff + skin
        self.neighbors: List[List[int]] = []
        self.ref_pos: List[Vec3] = []

    def build(self, positions: List[Vec3]) -> None:
        n = len(positions)
        self.neighbors = [[] for _ in range(n)]
        self.ref_pos = positions[:]
        r2 = self.r_list * self.r_list
        for i in range(n):
            for j in range(i + 1, n):
                dx = positions[i][0] - positions[j][0]
                dy = positions[i][1] - positions[j][1]
                dz = positions[i][2] - positions[j][2]
                if dx*dx + dy*dy + dz*dz <= r2:
                    self.neighbors[i].append(j)
                    self.neighbors[j].append(i)

    def needs_rebuild(self, positions: List[Vec3]) -> bool:
        max_disp = 0.0
        for i, p in enumerate(positions):
            dx = p[0] - self.ref_pos[i][0]
            dy = p[1] - self.ref_pos[i][1]
            dz = p[2] - self.ref_pos[i][2]
            disp = math.sqrt(dx*dx + dy*dy + dz*dz)
            if disp > max_disp:
                max_disp = disp
        return max_disp > self.skin * 0.5


if __name__ == "__main__":
    pos = [(0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (3.0, 0.0, 0.0)]
    vl = VerletList(cutoff=1.0, skin=0.5)
    vl.build(pos)
    assert 1 in vl.neighbors[0] and 0 in vl.neighbors[1]
    assert 2 not in vl.neighbors[0]
    print("verlet_list self-test passed")
