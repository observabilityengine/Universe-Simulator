"""Union-Find (Disjoint Set Union) with path compression + union by rank.

Complexity: O(alpha(n)) per operation. Original implementation.
"""
from __future__ import annotations

class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

if __name__ == "__main__":
    uf = UnionFind(10)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.connected(0, 2)
    assert not uf.connected(0, 3)
    assert uf.count == 7
    print("union_find self-tests passed")
