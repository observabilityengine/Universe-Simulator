"""
Universe Simulator - Densest Subgraph (Charikar greedy)
Original 2-approximation by peeling minimum-degree vertices.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

def densest_subgraph(graph: Dict[int, List[int]]) -> Tuple[Set[int], float]:
    adj = {u: set(vs) for u, vs in graph.items()}
    for u in list(adj):
        for v in adj[u]:
            adj.setdefault(v, set()).add(u)
    remaining = set(adj.keys())
    degrees = {u: len(adj[u]) for u in remaining}
    best_density = 0.0
    best_set = set()
    order = []
    while remaining:
        edges = sum(degrees[u] for u in remaining) / 2
        density = edges / len(remaining) if remaining else 0
        if density > best_density:
            best_density = density
            best_set = remaining.copy()
        u = min(remaining, key=lambda x: degrees[x])
        order.append(u)
        for v in adj[u]:
            if v in remaining:
                degrees[v] -= 1
        remaining.remove(u)
    return best_set, best_density

if __name__ == "__main__":
    g = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2]}
    s, d = densest_subgraph(g)
    assert d >= 1.0
    print("densest_subgraph self-test passed", d)
