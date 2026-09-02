"""
Module 70 – Bellman-Ford Shortest Path
Handles negative weights and detects negative cycles.
Complete implementation.
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Hashable, Optional


def bellman_ford(
    edges: List[Tuple[Hashable, Hashable, float]],
    source: Hashable,
    nodes: Optional[List[Hashable]] = None,
) -> Tuple[Optional[Dict[Hashable, float]], bool]:
    if nodes is None:
        nodes = list({u for u, v, w in edges} | {v for u, v, w in edges})
    dist = {n: float("inf") for n in nodes}
    dist[source] = 0.0
    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None, True
    return dist, False


if __name__ == "__main__":
    print("Testing Bellman-Ford...")
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", -1),
        ("B", "D", 5), ("C", "D", 3), ("C", "E", 2), ("D", "E", -2),
    ]
    dist, neg = bellman_ford(edges, "A")
    print(f"  Negative cycle: {neg}")
    print(f"  Distances: { {k: round(v,1) for k,v in dist.items()} }")
    edges_neg = edges + [("E", "B", -6)]
    dist2, neg2 = bellman_ford(edges_neg, "A")
    print(f"  With neg cycle: dist={dist2} neg={neg2}")
    print("Bellman-Ford module OK.")
