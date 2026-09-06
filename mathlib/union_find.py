"""Union-Find (Disjoint Set Union) with path compression and union-by-rank.

Complexity: nearly O(1) amortized (inverse Ackermann).
"""
from __future__ import annotations

from typing import Dict, List, Hashable


class UnionFind:
    def __init__(self, elements: List[Hashable] | None = None):
        self.parent: Dict[Hashable, Hashable] = {}
        self.rank: Dict[Hashable, int] = {}
        if elements:
            for e in elements:
                self.make_set(e)

    def make_set(self, x: Hashable) -> None:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x: Hashable) -> Hashable:
        if x not in self.parent:
            self.make_set(x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Hashable, y: Hashable) -> bool:
        """Return True if a merge occurred."""
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


if __name__ == "__main__":
    uf = UnionFind([0, 1, 2, 3])
    assert uf.union(0, 1)
    assert uf.connected(0, 1)
    assert not uf.connected(0, 2)
    uf.union(1, 2)
    assert uf.connected(0, 2)
    assert not uf.union(0, 2)
    uf2 = UnionFind()
    uf2.union("a", "b")
    assert uf2.connected("a", "b")
    uf0 = UnionFind([])
    assert uf0.find(99) == 99
    print("union_find self-tests passed")
