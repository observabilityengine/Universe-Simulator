"""
Universe Simulator - Kosaraju SCC
Original two-pass DFS.
"""

from __future__ import annotations

from typing import Dict, List, Set

def kosaraju(graph: Dict[int, List[int]]) -> List[List[int]]:
    nodes = list(graph.keys())
    visited: Set[int] = set()
    order: List[int] = []

    def dfs1(u: int) -> None:
        visited.add(u)
        for v in graph.get(u, []):
            if v not in visited:
                dfs1(v)
        order.append(u)

    for u in nodes:
        if u not in visited:
            dfs1(u)

    rev: Dict[int, List[int]] = {u: [] for u in nodes}
    for u in graph:
        for v in graph[u]:
            rev.setdefault(v, []).append(u)

    visited.clear()
    components: List[List[int]] = []

    def dfs2(u: int, comp: List[int]) -> None:
        visited.add(u)
        comp.append(u)
        for v in rev.get(u, []):
            if v not in visited:
                dfs2(v, comp)

    for u in reversed(order):
        if u not in visited:
            comp: List[int] = []
            dfs2(u, comp)
            components.append(comp)
    return components

if __name__ == "__main__":
    g = {0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [3]}
    sccs = kosaraju(g)
    assert any(set(c) == {0, 1, 2} for c in sccs)
    print("kosaraju self-test passed", sccs)
