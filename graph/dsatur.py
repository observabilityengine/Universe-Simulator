"""DSATUR graph coloring algorithm.

Complexity: O(n^2). Original implementation.
"""
from __future__ import annotations

from typing import List, Set, Tuple


def dsatur_coloring(
    n: int,
    edges: List[Tuple[int, int]],
) -> List[int]:
    """Color an undirected graph with DSATUR heuristic. Returns color assignment."""
    adj: List[Set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)

    color = [-1] * n
    saturation = [0] * n
    degree = [len(adj[i]) for i in range(n)]
    uncolored = set(range(n))

    while uncolored:
        v = max(uncolored, key=lambda i: (saturation[i], degree[i]))
        used = {color[u] for u in adj[v] if color[u] >= 0}
        c = 0
        while c in used:
            c += 1
        color[v] = c
        uncolored.remove(v)
        for u in adj[v]:
            if color[u] < 0:
                neigh_colors = {color[w] for w in adj[u] if color[w] >= 0}
                saturation[u] = len(neigh_colors)
    return color


if __name__ == "__main__":
    path = [(0, 1), (1, 2), (2, 3)]
    col = dsatur_coloring(4, path)
    assert len(set(col)) <= 2
    assert col[0] != col[1] and col[1] != col[2]
    k3 = [(0, 1), (1, 2), (0, 2)]
    col3 = dsatur_coloring(3, k3)
    assert len(set(col3)) == 3
    assert dsatur_coloring(3, []) == [0, 0, 0]
    print("dsatur self-tests passed")
