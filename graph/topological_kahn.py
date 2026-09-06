"""Kahn's algorithm for topological sort (BFS-based).

Complexity: O(V + E).
Returns list of nodes in topo order, or empty list if cycle exists.
Original implementation.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, Hashable, List


def topological_kahn(adj: Dict[Hashable, List[Hashable]]) -> List[Hashable]:
    """Topological order via Kahn. Empty result means cycle (or empty graph)."""
    indeg: Dict[Hashable, int] = {}
    nodes = set(adj.keys())
    for u, vs in adj.items():
        indeg.setdefault(u, 0)
        for v in vs:
            nodes.add(v)
            indeg[v] = indeg.get(v, 0) + 1
            indeg.setdefault(u, 0)
    for u in nodes:
        indeg.setdefault(u, 0)
    q = deque([u for u in nodes if indeg[u] == 0])
    order: List[Hashable] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(nodes):
        return []  # cycle
    return order


if __name__ == "__main__":
    adj = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    order = topological_kahn(adj)
    assert order.index("A") < order.index("B")
    assert order.index("B") < order.index("D")
    assert order.index("C") < order.index("D")
    cycle = {"A": ["B"], "B": ["A"]}
    assert topological_kahn(cycle) == []
    assert topological_kahn({}) == []
    assert topological_kahn({"X": []}) == ["X"]
    print("topological_kahn self-tests passed")
