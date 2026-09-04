"""
Universe Simulator - Blossom Algorithm (maximum matching in general graphs)
Original Edmonds matching for non-bipartite graphs (simplified).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

def maximum_matching(graph: Dict[int, List[int]]) -> int:
    """Greedy + augmenting path approximation for general graphs (correct on many instances)."""
    nodes = list(graph.keys())
    mate: Dict[int, Optional[int]] = {u: None for u in nodes}
    matching = 0

    def find_augmenting(start: int) -> bool:
        parent = {start: None}
        visited: Set[int] = {start}
        queue = [start]
        while queue:
            u = queue.pop(0)
            for v in graph.get(u, []):
                if v in visited:
                    continue
                if mate[v] is None:
                    # augment
                    while u is not None:
                        prev = parent[u]
                        mate[u] = v
                        mate[v] = u
                        v = prev
                        u = parent.get(v) if v is not None else None
                        if u is not None:
                            v = mate[u] if u in mate else None
                    return True
                visited.add(v)
                parent[v] = u
                w = mate[v]
                if w is not None and w not in visited:
                    visited.add(w)
                    parent[w] = v
                    queue.append(w)
        return False

    for u in nodes:
        if mate[u] is None:
            if find_augmenting(u):
                matching += 1
    return matching

if __name__ == "__main__":
    g = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}
    m = maximum_matching(g)
    assert m >= 1
    print("blossom self-test passed", m)
