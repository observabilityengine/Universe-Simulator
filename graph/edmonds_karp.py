"""
Universe Simulator - Edmonds-Karp Max Flow
Original BFS-based Ford-Fulkerson.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Tuple


def edmonds_karp(
    capacity: Dict[int, Dict[int, float]],
    source: int,
    sink: int,
) -> float:
    flow = 0.0
    residual = {u: dict(v) for u, v in capacity.items()}
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
            residual[v].setdefault(u, 0.0)

    while True:
        parent: Dict[int, int] = {}
        q = deque([source])
        parent[source] = -1
        found = False
        while q and not found:
            u = q.popleft()
            for v, cap in residual.get(u, {}).items():
                if v not in parent and cap > 1e-12:
                    parent[v] = u
                    if v == sink:
                        found = True
                        break
                    q.append(v)
        if not found:
            break
        # bottleneck
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u
        flow += path_flow
    return flow


if __name__ == "__main__":
    cap = {
        0: {1: 10, 2: 5},
        1: {2: 15, 3: 5},
        2: {3: 10},
        3: {},
    }
    mf = edmonds_karp(cap, 0, 3)
    assert abs(mf - 15.0) < 1e-6
    print("edmonds_karp self-test passed", mf)
