"""Breadth-first search on adjacency-list graphs.

Complexity: O(V + E).
Returns distances from source (unweighted) and parent pointers.
Unreachable nodes get dist = -1. Original implementation.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, Hashable, List, Tuple


def bfs(
    adj: Dict[Hashable, List[Hashable]],
    source: Hashable,
) -> Tuple[Dict[Hashable, int], Dict[Hashable, Hashable]]:
    """BFS from source. Returns (dist, parent)."""
    dist: Dict[Hashable, int] = {source: 0}
    parent: Dict[Hashable, Hashable] = {}
    q: deque[Hashable] = deque([source])
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
    return dist, parent


if __name__ == "__main__":
    adj = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    dist, parent = bfs(adj, "A")
    assert dist["A"] == 0 and dist["B"] == 1 and dist["D"] == 2
    assert parent["D"] in ("B", "C")
    dist2, _ = bfs(adj, "D")
    assert dist2 == {"D": 0}
    dist3, _ = bfs({}, "X")
    assert dist3 == {"X": 0}
    print("bfs self-tests passed")
