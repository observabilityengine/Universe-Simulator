"""Connected components in undirected graph (DFS).

Complexity: O(V + E).
Returns list of components (each a list of nodes). Original implementation.
"""
from __future__ import annotations

from typing import Dict, Hashable, List, Set


def connected_components(adj: Dict[Hashable, List[Hashable]]) -> List[List[Hashable]]:
    """Return connected components of undirected graph."""
    nodes: Set[Hashable] = set(adj.keys())
    for vs in adj.values():
        nodes.update(vs)
    visited: Set[Hashable] = set()
    components: List[List[Hashable]] = []

    def dfs(u: Hashable, comp: List[Hashable]) -> None:
        visited.add(u)
        comp.append(u)
        for v in adj.get(u, []):
            if v not in visited:
                dfs(v, comp)

    for u in nodes:
        if u not in visited:
            comp: List[Hashable] = []
            dfs(u, comp)
            components.append(comp)
    return components


if __name__ == "__main__":
    adj = {"A": ["B"], "B": ["A", "C"], "C": ["B"], "D": ["E"], "E": ["D"], "F": []}
    comps = connected_components(adj)
    assert len(comps) == 3
    sizes = sorted(len(c) for c in comps)
    assert sizes == [1, 2, 3]
    assert connected_components({}) == []
    assert len(connected_components({"X": []})) == 1
    print("connected_components self-tests passed")
