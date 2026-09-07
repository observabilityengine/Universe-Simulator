"""Dinic's algorithm for maximum flow.

Complexity: O(V^2 E) worst-case. Original implementation.
"""
from __future__ import annotations

from collections import deque
from typing import List, Tuple


class _Edge:
    __slots__ = ("to", "rev", "cap")

    def __init__(self, to: int, rev: int, cap: int) -> None:
        self.to = to
        self.rev = rev
        self.cap = cap


class Dinic:
    """Maximum flow using Dinic's blocking-flow algorithm."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.graph: List[List[_Edge]] = [[] for _ in range(n)]
        self.level: List[int] = []
        self.ptr: List[int] = []

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        if capacity <= 0:
            return
        fwd = _Edge(v, len(self.graph[v]), capacity)
        rev = _Edge(u, len(self.graph[u]), 0)
        self.graph[u].append(fwd)
        self.graph[v].append(rev)

    def _bfs(self, source: int, sink: int) -> bool:
        self.level = [-1] * self.n
        self.level[source] = 0
        q: deque[int] = deque([source])
        while q:
            u = q.popleft()
            for e in self.graph[u]:
                if e.cap > 0 and self.level[e.to] < 0:
                    self.level[e.to] = self.level[u] + 1
                    q.append(e.to)
        return self.level[sink] >= 0

    def _dfs(self, u: int, sink: int, pushed: int) -> int:
        if u == sink or pushed == 0:
            return pushed
        while self.ptr[u] < len(self.graph[u]):
            e = self.graph[u][self.ptr[u]]
            if e.cap > 0 and self.level[e.to] == self.level[u] + 1:
                tr = self._dfs(e.to, sink, min(pushed, e.cap))
                if tr > 0:
                    e.cap -= tr
                    self.graph[e.to][e.rev].cap += tr
                    return tr
            self.ptr[u] += 1
        return 0

    def max_flow(self, source: int, sink: int) -> int:
        flow = 0
        while self._bfs(source, sink):
            self.ptr = [0] * self.n
            while True:
                pushed = self._dfs(source, sink, 10**18)
                if pushed == 0:
                    break
                flow += pushed
        return flow


def dinic_max_flow(
    n: int,
    edges: List[Tuple[int, int, int]],
    source: int,
    sink: int,
) -> int:
    """Convenience wrapper: edges = [(u, v, capacity), ...]."""
    g = Dinic(n)
    for u, v, c in edges:
        g.add_edge(u, v, c)
    return g.max_flow(source, sink)


if __name__ == "__main__":
    edges = [
        (0, 1, 10), (0, 2, 10),
        (1, 2, 2), (1, 3, 4), (1, 4, 8),
        (2, 4, 9),
        (3, 5, 10),
        (4, 3, 6), (4, 5, 10),
    ]
    flow = dinic_max_flow(6, edges, 0, 5)
    assert flow == 19, flow
    assert dinic_max_flow(3, [(0, 1, 5)], 0, 2) == 0
    assert dinic_max_flow(2, [(0, 1, 7)], 0, 1) == 7
    edges2 = [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 2), (2, 3, 4)]
    assert dinic_max_flow(4, edges2, 0, 3) == 5
    print("dinic self-tests passed")
