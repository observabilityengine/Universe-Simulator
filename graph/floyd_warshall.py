"""
Universe Simulator - Floyd-Warshall All-Pairs Shortest Paths
Original dense implementation with path reconstruction support.
"""

from __future__ import annotations

import math
from typing import List, Optional


def floyd_warshall(n: int, edges: List[tuple]) -> List[List[float]]:
    """
    edges: list of (u, v, weight)
    Returns dist matrix. Uses math.inf for unreachable.
    """
    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


if __name__ == "__main__":
    edges = [(0, 1, 3.0), (1, 2, 1.0), (0, 2, 10.0), (2, 0, 2.0)]
    d = floyd_warshall(3, edges)
    assert abs(d[0][2] - 4.0) < 1e-9
    print("floyd_warshall self-test passed", d)
