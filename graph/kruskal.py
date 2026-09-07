"""Kruskal's MST algorithm with Union-Find.

Complexity: O(E log E). Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple


class _UF:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        return True


def kruskal(n: int, edges: List[Tuple[int, int, float]]) -> Tuple[List[Tuple[int, int, float]], float]:
    edges = sorted(edges, key=lambda e: e[2])
    uf = _UF(n)
    mst = []
    weight = 0.0
    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            weight += w
            if len(mst) == n - 1:
                break
    return mst, weight


if __name__ == "__main__":
    edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 1)]
    mst, w = kruskal(4, edges)
    assert len(mst) == 3
    assert abs(w - 4.0) < 1e-9
    print("kruskal self-tests passed")
