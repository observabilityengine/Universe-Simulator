"""Kahn's algorithm for topological sort of a DAG.

Complexity: O(V + E).
Assumes directed graph; raises ValueError on cycle detection.
Returns one valid linear order; empty list for empty graph.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, List, Set


def topological_sort(graph: Dict[int, List[int]]) -> List[int]:
    """Return a topological ordering of the nodes.

    Parameters
    ----------
    graph : adjacency list node -> list of successors (directed)

    Returns
    -------
    list of nodes in topological order

    Raises
    ------
    ValueError if a cycle exists
    """
    nodes: Set[int] = set(graph.keys())
    for succs in graph.values():
        nodes.update(succs)
    indeg = {n: 0 for n in nodes}
    for u in graph:
        for v in graph[u]:
            indeg[v] = indeg.get(v, 0) + 1

    q = deque([n for n in nodes if indeg[n] == 0])
    order: List[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) != len(nodes):
        raise ValueError("graph contains a cycle")
    return order


if __name__ == "__main__":
    g = {0: [1, 2], 1: [3], 2: [3], 3: []}
    order = topological_sort(g)
    assert order.index(0) < order.index(1)
    assert order.index(0) < order.index(2)
    assert order.index(1) < order.index(3)
    assert order.index(2) < order.index(3)

    # Empty
    assert topological_sort({}) == []

    # Single
    assert topological_sort({5: []}) == [5]

    # Linear chain
    g2 = {i: [i + 1] for i in range(5)}
    g2[5] = []
    assert topological_sort(g2) == list(range(6))

    # Cycle must raise
    try:
        topological_sort({0: [1], 1: [0]})
        assert False, "should have raised"
    except ValueError:
        pass

    # Disconnected DAG
    g3 = {0: [1], 2: [3], 1: [], 3: []}
    order3 = topological_sort(g3)
    assert set(order3) == {0, 1, 2, 3}
    assert order3.index(0) < order3.index(1)
    assert order3.index(2) < order3.index(3)

    print("topological_sort self-tests passed")
