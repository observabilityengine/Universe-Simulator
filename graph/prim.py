"""
Universe Simulator - Prim MST (dense O(n^2))
Original implementation.
"""

from __future__ import annotations

import math
from typing import List, Tuple


def prim(n: int, adj: List[List[float]]) -> Tuple[float, List[int]]:
    """adj[i][j] = weight or math.inf if no edge. Returns (total, parent)."""
    key = [math.inf] * n
    parent = [-1] * n
    in_mst = [False] * n
    key[0] = 0.0
    for _ in range(n):
        u = min((i for i in range(n) if not in_mst[i]), key=lambda i: key[i])
        in_mst[u] = True
        for v in range(n):
            if not in_mst[v] and adj[u][v] < key[v]:
                key[v] = adj[u][v]
                parent[v] = u
    total = sum(key[i] for i in range(1, n) if key[i] < math.inf)
    return total, parent


if __name__ == "__main__":
    INF = math.inf
    adj = [
        [0, 4, 3, INF],
        [4, 0, 1, 2],
        [3, 1, 0, 5],
        [INF, 2, 5, 0],
    ]
    cost, par = prim(4, adj)
    assert abs(cost - 6.0) < 1e-9
    print("prim self-test passed", cost, par)
