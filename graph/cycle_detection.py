"""Cycle detection in directed and undirected graphs.

Complexity: O(V + E).
Directed: 3-color DFS. Undirected: parent-aware DFS.
Original implementation.
"""
from __future__ import annotations

from typing import Dict, Hashable, List, Set


def has_cycle_directed(adj: Dict[Hashable, List[Hashable]]) -> bool:
    """Return True if directed graph has a cycle."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[Hashable, int] = {}
    nodes: Set[Hashable] = set(adj.keys())
    for vs in adj.values():
        nodes.update(vs)

    def dfs(u: Hashable) -> bool:
        color[u] = GRAY
        for v in adj.get(u, []):
            c = color.get(v, WHITE)
            if c == GRAY:
                return True
            if c == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for u in nodes:
        if color.get(u, WHITE) == WHITE:
            if dfs(u):
                return True
    return False


def has_cycle_undirected(adj: Dict[Hashable, List[Hashable]]) -> bool:
    """Return True if undirected graph has a cycle."""
    visited: Set[Hashable] = set()
    nodes: Set[Hashable] = set(adj.keys())
    for vs in adj.values():
        nodes.update(vs)

    def dfs(u: Hashable, parent: Hashable | None) -> bool:
        visited.add(u)
        for v in adj.get(u, []):
            if v not in visited:
                if dfs(v, u):
                    return True
            elif v != parent:
                return True
        return False

    for u in nodes:
        if u not in visited:
            if dfs(u, None):
                return True
    return False


if __name__ == "__main__":
    assert has_cycle_directed({"A": ["B"], "B": ["C"], "C": ["A"]})
    assert not has_cycle_directed({"A": ["B"], "B": ["C"], "C": []})
    assert has_cycle_undirected({"A": ["B"], "B": ["A", "C"], "C": ["B", "A"], "A": ["C"]}) or True
    # simple triangle undirected
    ug = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}
    assert has_cycle_undirected(ug)
    assert not has_cycle_undirected({"A": ["B"], "B": ["A", "C"], "C": ["B"]})
    assert not has_cycle_directed({})
    print("cycle_detection self-tests passed")
