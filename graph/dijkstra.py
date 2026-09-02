"""
Module 57 – Dijkstra Shortest Path
Binary-heap Dijkstra for weighted directed graphs.
Complete implementation.
"""

from __future__ import annotations
import heapq
from typing import Dict, List, Tuple, Hashable, Optional


class Graph:
    def __init__(self):
        self.adj: Dict[Hashable, List[Tuple[Hashable, float]]] = {}

    def add_edge(self, u: Hashable, v: Hashable, weight: float) -> None:
        if weight < 0:
            raise ValueError("Dijkstra requires non-negative weights")
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append((v, weight))
        if v not in self.adj:
            self.adj[v] = []

    def dijkstra(self, source: Hashable) -> Tuple[Dict[Hashable, float], Dict[Hashable, Hashable]]:
        dist = {source: 0.0}
        prev: Dict[Hashable, Hashable] = {}
        pq: List[Tuple[float, Hashable]] = [(0.0, source)]
        visited = set()

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            for v, w in self.adj.get(u, []):
                nd = d + w
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, prev

    def shortest_path(self, source: Hashable, target: Hashable) -> Optional[List[Hashable]]:
        dist, prev = self.dijkstra(source)
        if target not in dist:
            return None
        path = []
        cur = target
        while cur != source:
            path.append(cur)
            cur = prev[cur]
        path.append(source)
        path.reverse()
        return path


if __name__ == "__main__":
    print("Testing Dijkstra...")
    g = Graph()
    edges = [
        ("A", "B", 4), ("A", "C", 2),
        ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    dist, _ = g.dijkstra("A")
    print(f"  Distances from A: { {k: round(v,1) for k,v in dist.items()} }")
    path = g.shortest_path("A", "F")
    print(f"  Path A\u2192F: {path}")
    print("Dijkstra module OK.")
