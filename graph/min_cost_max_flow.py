"""
Universe Simulator - Min-Cost Max-Flow (successive shortest paths with potentials)
Original implementation using reduced costs.
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import heapq

def min_cost_max_flow(
    capacity: Dict[int, Dict[int, float]],
    cost: Dict[int, Dict[int, float]],
    source: int,
    sink: int,
) -> Tuple[float, float]:
    residual = {u: dict(vs) for u, vs in capacity.items()}
    res_cost = {u: dict(vs) for u, vs in cost.items()}
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
            residual[v].setdefault(u, 0.0)
            res_cost.setdefault(v, {})
            res_cost[v].setdefault(u, -cost[u][v])

    flow = cost_sum = 0.0
    pot = {u: 0.0 for u in residual}

    while True:
        dist = {source: 0.0}
        parent = {}
        pq = [(0.0, source)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist.get(u, float("inf")):
                continue
            for v, cap in residual.get(u, {}).items():
                if cap > 1e-12:
                    reduced = res_cost[u][v] + pot[u] - pot.get(v, 0.0)
                    nd = d + reduced
                    if nd < dist.get(v, float("inf")) - 1e-12:
                        dist[v] = nd
                        parent[v] = u
                        heapq.heappush(pq, (nd, v))
        if sink not in parent:
            break
        for u in residual:
            if u in dist:
                pot[u] += dist[u]
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
            cost_sum += path_flow * res_cost[u][v]
            v = u
        flow += path_flow
    return flow, cost_sum

if __name__ == "__main__":
    cap = {0: {1: 2, 2: 1}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    cst = {0: {1: 1, 2: 3}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    f, c = min_cost_max_flow(cap, cst, 0, 3)
    assert abs(f - 2.0) < 1e-6
    print("min_cost_max_flow self-test passed", f, c)
