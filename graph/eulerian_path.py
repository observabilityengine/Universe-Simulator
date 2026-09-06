"""Hierholzer's algorithm for Eulerian path in directed multigraph.

Complexity: O(E).
Returns node path or empty if none exists. Original implementation.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, Hashable, List


def eulerian_path_directed(
    edges: List[tuple[Hashable, Hashable]],
) -> List[Hashable]:
    """Return Eulerian path as node list, or [] if impossible."""
    adj: Dict[Hashable, List[Hashable]] = defaultdict(list)
    indeg: Dict[Hashable, int] = defaultdict(int)
    outdeg: Dict[Hashable, int] = defaultdict(int)
    nodes = set()
    for u, v in edges:
        adj[u].append(v)
        outdeg[u] += 1
        indeg[v] += 1
        nodes.add(u)
        nodes.add(v)
    if not edges:
        return []
    start_candidates = []
    end_candidates = []
    for u in nodes:
        diff = outdeg[u] - indeg[u]
        if diff == 1:
            start_candidates.append(u)
        elif diff == -1:
            end_candidates.append(u)
        elif diff != 0:
            return []
    if len(start_candidates) > 1 or len(end_candidates) > 1:
        return []
    start = start_candidates[0] if start_candidates else next(iter(nodes))
    stack = [start]
    path: List[Hashable] = []
    local_adj = {u: list(vs) for u, vs in adj.items()}
    while stack:
        u = stack[-1]
        if local_adj.get(u):
            stack.append(local_adj[u].pop())
        else:
            path.append(stack.pop())
    path.reverse()
    if len(path) != len(edges) + 1:
        return []
    return path


if __name__ == "__main__":
    edges = [(0, 1), (1, 2), (2, 0), (0, 3)]
    path = eulerian_path_directed(edges)
    assert len(path) == 5
    # verify edges used
    used = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    assert sorted(used) == sorted(edges)
    assert eulerian_path_directed([]) == []
    print("eulerian_path self-tests passed")
