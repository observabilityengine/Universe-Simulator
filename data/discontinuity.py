"""
Universe Simulator - Disjoint Set with Continuity Tracking (simple)
Original Union-Find with component size and max element.
"""

from __future__ import annotations

from typing import Dict

class DSU:
    def __init__(self) -> None:
        self.parent: Dict[int, int] = {}
        self.size: Dict[int, int] = {}
        self.max_val: Dict[int, int] = {}

    def add(self, x: int) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
            self.max_val[x] = x

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.max_val[ra] = max(self.max_val[ra], self.max_val[rb])

if __name__ == "__main__":
    d = DSU()
    for i in range(5):
        d.add(i)
    d.union(0, 1)
    d.union(2, 3)
    d.union(1, 2)
    assert d.find(0) == d.find(3)
    assert d.size[d.find(0)] == 4
    print("discontinuity self-test passed")
