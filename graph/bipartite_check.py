"""Bipartite check via BFS 2-coloring.

Complexity: O(V + E).
Returns (is_bipartite, coloring dict). Original implementation.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, Hashable, List, Optional, Tuple


def is_bipartite(
    adj: Dict[Hashable, List[Hashable]],
) -> Tuple[bool, Dict[Hashable, int]]:
    """Return (True, color) if bipartite; color maps node → 0/1."""
    color: Dict[Hashable, int] = {}
    nodes = set(adj.keys())
    for vs in adj.values():
        nodes.update(vs)
    for start in nodes:
        if start in color:
            continue
        color[start] = 0
        q: deque[Hashable] = deque([start])
        while q:
            u = q.popleft()
            for v in adj.get(u, []):
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, color
    return True, color


if __name__ == "__main__":
    ok, c = is_bipartite({"A": ["B"], "B": ["A", "C"], "C": ["B"]})
    assert ok and c["A"] != c["B"]
    triangle = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}
    bad, _ = is_bipartite(triangle)
    assert not bad
    assert is_bipartite({})[0]
    print("bipartite_check self-tests passed")
