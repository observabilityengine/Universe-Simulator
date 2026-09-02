"""
Module 45 – Union-Find (Disjoint Set)
Path compression + union by rank.
Original implementation.
"""

from __future__ import annotations
from typing import Hashable, Dict


class UnionFind:
    def __init__(self):
        self.parent: Dict[Hashable, Hashable] = {}
        self.rank: Dict[Hashable, int] = {}

    def find(self, x: Hashable) -> Hashable:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            return x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Hashable, y: Hashable) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

    def connected(self, x: Hashable, y: Hashable) -> bool:
        return self.find(x) == self.find(y)

    def components(self) -> int:
        return len({self.find(x) for x in self.parent})


if __name__ == "__main__":
    print("Testing Union-Find...")
    uf = UnionFind()
    uf.union("a", "b")
    uf.union("b", "c")
    uf.union("d", "e")
    print(f"  a-c connected: {uf.connected('a', 'c')}")
    print(f"  a-d connected: {uf.connected('a', 'd')}")
    print(f"  components: {uf.components()}")
    uf.union("c", "d")
    print(f"  after union c-d components: {uf.components()}")
    print("Union-Find module OK.")
