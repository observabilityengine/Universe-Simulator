"""
Universe Simulator - Kruskal MST
Original Union-Find based Kruskal.
"""

from __future__ import annotations

from typing import List, Tuple


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True


def kruskal(n: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int, float]]]:
    edges = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(n)
    mst = []
    total = 0.0
    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:
                break
    return total, mst


if __name__ == "__main__":
    edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 5)]
    cost, mst = kruskal(4, edges)
    assert abs(cost - 6.0) < 1e-9
    print("kruskal self-test passed", cost, mst)
