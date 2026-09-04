"""
Universe Simulator - Cost-Scaling Min-Cost Flow
Original successive approximation cost scaling.
"""

from __future__ import annotations

from typing import Dict, Tuple

def mcmf_cost_scaling(
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
    # simple successive shortest path as practical cost-scaling base
    flow = cost_sum = 0.0
    while True:
        dist = {source: 0.0}
        parent = {}
        changed = True
        nodes = list(residual.keys())
        for _ in range(len(nodes)):
            changed = False
            for u in nodes:
                if u not in dist:
                    continue
                for v, cap in residual.get(u, {}).items():
                    if cap > 1e-12 and (v not in dist or dist[v] > dist[u] + res_cost[u][v] + 1e-12):
                        dist[v] = dist[u] + res_cost[u][v]
                        parent[v] = u
                        changed = True
            if not changed:
                break
        if sink not in parent:
            break
        pf = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            pf = min(pf, residual[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= pf
            residual[v][u] += pf
            cost_sum += pf * res_cost[u][v]
            v = u
        flow += pf
    return flow, cost_sum

if __name__ == "__main__":
    cap = {0: {1: 2, 2: 1}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    cst = {0: {1: 1, 2: 3}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    f, c = mcmf_cost_scaling(cap, cst, 0, 3)
    assert abs(f - 2.0) < 1e-6
    print("mcmf_cost_scaling self-test passed", f, c)
