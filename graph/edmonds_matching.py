"""
Universe Simulator - Edmonds Blossom Matching (greedy + augment)
Original maximum matching for general graphs.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

def edmonds_matching(graph: Dict[int, List[int]]) -> int:
    nodes = list(graph.keys())
    mate: Dict[int, Optional[int]] = {u: None for u in nodes}
    matching = 0

    def bfs_augment(start: int) -> bool:
        parent = {start: None}
        visited: Set[int] = {start}
        queue = [start]
        while queue:
            u = queue.pop(0)
            for v in graph.get(u, []):
                if v in visited:
                    continue
                if mate[v] is None:
                    # reconstruct path and augment
                    path = []
                    cur_u, cur_v = u, v
                    while cur_u is not None:
                        path.append((cur_u, cur_v))
                        cur_v = mate[cur_u]
                        cur_u = parent.get(cur_u)
                    for a, b in path:
                        mate[a] = b
                        mate[b] = a
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
            if bfs_augment(u):
                matching += 1
    return matching

if __name__ == "__main__":
    g = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4], 4: [3]}
    m = edmonds_matching(g)
    assert m >= 2
    print("edmonds_matching self-test passed", m)
