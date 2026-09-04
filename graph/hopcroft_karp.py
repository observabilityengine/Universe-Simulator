"""
Universe Simulator - Hopcroft-Karp Maximum Bipartite Matching
Original implementation.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional

def hopcroft_karp(graph: Dict[int, List[int]], left: List[int], right: List[int]) -> int:
    pair_u: Dict[int, Optional[int]] = {u: None for u in left}
    pair_v: Dict[int, Optional[int]] = {v: None for v in right}
    dist: Dict[int, int] = {}

    def bfs() -> bool:
        q = deque()
        for u in left:
            if pair_u[u] is None:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = float("inf")
        dist[None] = float("inf")
        while q:
            u = q.popleft()
            if dist[u] < dist[None]:
                for v in graph.get(u, []):
                    pu = pair_v[v]
                    if dist.get(pu, float("inf")) == float("inf"):
                        dist[pu] = dist[u] + 1
                        q.append(pu)
        return dist[None] != float("inf")

    def dfs(u: int) -> bool:
        if u is not None:
            for v in graph.get(u, []):
                pu = pair_v[v]
                if dist.get(pu, float("inf")) == dist[u] + 1 and dfs(pu):
                    pair_v[v] = u
                    pair_u[u] = v
                    return True
            dist[u] = float("inf")
            return False
        return True

    matching = 0
    while bfs():
        for u in left:
            if pair_u[u] is None and dfs(u):
                matching += 1
    return matching

if __name__ == "__main__":
    g = {0: [0, 1], 1: [1, 2], 2: [0]}
    m = hopcroft_karp(g, [0, 1, 2], [0, 1, 2])
    assert m == 2
    print("hopcroft_karp self-test passed", m)
