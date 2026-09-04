"""
Universe Simulator - Successive Shortest Path Min-Cost Max-Flow
Original SPFA-based implementation.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Tuple

def min_cost_flow(
    capacity: Dict[int, Dict[int, float]],
    cost: Dict[int, Dict[int, float]],
    source: int,
    sink: int,
    max_flow: float = float("inf"),
) -> Tuple[float, float]:
    residual_cap = {u: dict(vs) for u, vs in capacity.items()}
    residual_cost = {u: dict(vs) for u, vs in cost.items()}
    for u in list(residual_cap):
        for v in residual_cap[u]:
            residual_cap.setdefault(v, {})
            residual_cap[v].setdefault(u, 0.0)
            residual_cost.setdefault(v, {})
            residual_cost[v].setdefault(u, -cost[u][v])

    flow = cost_sum = 0.0
    while flow < max_flow:
        # SPFA
        dist = {source: 0.0}
        parent = {}
        in_queue = {source}
        q = deque([source])
        while q:
            u = q.popleft()
            in_queue.discard(u)
            for v, cap in residual_cap.get(u, {}).items():
                if cap > 1e-12:
                    nd = dist[u] + residual_cost[u][v]
                    if v not in dist or nd < dist[v] - 1e-12:
                        dist[v] = nd
                        parent[v] = u
                        if v not in in_queue:
                            q.append(v)
                            in_queue.add(v)
        if sink not in parent:
            break
        # bottleneck
        path_flow = max_flow - flow
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual_cap[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual_cap[u][v] -= path_flow
            residual_cap[v][u] += path_flow
            cost_sum += path_flow * residual_cost[u][v]
            v = u
        flow += path_flow
    return flow, cost_sum

if __name__ == "__main__":
    cap = {0: {1: 2, 2: 1}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    cst = {0: {1: 1, 2: 2}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    f, c = min_cost_flow(cap, cst, 0, 3)
    assert abs(f - 2.0) < 1e-6
    print("min_cost_flow self-test passed", f, c)
