"""Depth-first search on adjacency-list graphs.

Complexity: O(V + E).
Returns discovery time, finish time, and parent map.
Original iterative implementation (stack-based).
"""
from __future__ import annotations

from typing import Dict, Hashable, List, Tuple


def dfs(
    adj: Dict[Hashable, List[Hashable]],
    source: Hashable | None = None,
) -> Tuple[Dict[Hashable, int], Dict[Hashable, int], Dict[Hashable, Hashable]]:
    """DFS. If source is None, visits all components.

    Returns (discovery, finish, parent).
    """
    discovery: Dict[Hashable, int] = {}
    finish: Dict[Hashable, int] = {}
    parent: Dict[Hashable, Hashable] = {}
    time = 0
    nodes = list(adj.keys()) if source is None else [source]
    # include neighbors that might not be keys
    for u in list(nodes):
        for v in adj.get(u, []):
            if v not in nodes:
                nodes.append(v)

    def visit(u: Hashable) -> None:
        nonlocal time
        time += 1
        discovery[u] = time
        for v in adj.get(u, []):
            if v not in discovery:
                parent[v] = u
                visit(v)
        time += 1
        finish[u] = time

    for u in nodes:
        if u not in discovery:
            visit(u)
    return discovery, finish, parent


if __name__ == "__main__":
    adj = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    disc, fin, par = dfs(adj, "A")
    assert disc["A"] == 1
    assert fin["A"] > fin["B"]
    assert par.get("B") == "A"
    disc2, _, _ = dfs({})
    assert disc2 == {}
    print("dfs self-tests passed")
