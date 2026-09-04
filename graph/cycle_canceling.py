"""
Universe Simulator - Cycle-Canceling Min-Cost Flow
Original successive negative-cycle cancellation.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

def cycle_canceling(
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

    # first max-flow (Edmonds-Karp style)
    def max_flow() -> float:
        flow = 0.0
        while True:
            parent = {}
            queue = [source]
            parent[source] = None
            found = False
            while queue and not found:
                u = queue.pop(0)
                for v, cap in residual.get(u, {}).items():
                    if v not in parent and cap > 1e-12:
                        parent[v] = u
                        if v == sink:
                            found = True
                            break
                        queue.append(v)
            if not found:
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
                v = u
            flow += pf
        return flow

    flow = max_flow()
    # cancel negative cycles (Bellman-Ford detection)
    cost_sum = 0.0
    nodes = list(residual.keys())
    for _ in range(len(nodes)):
        dist = {u: 0.0 for u in nodes}
        parent = {}
        for _ in range(len(nodes) - 1):
            for u in nodes:
                for v, cap in residual.get(u, {}).items():
                    if cap > 1e-12 and dist[v] > dist[u] + res_cost[u][v] + 1e-12:
                        dist[v] = dist[u] + res_cost[u][v]
                        parent[v] = u
        # find cycle
        cycle_node = None
        for u in nodes:
            for v, cap in residual.get(u, {}).items():
                if cap > 1e-12 and dist[v] > dist[u] + res_cost[u][v] + 1e-12:
                    cycle_node = v
                    break
            if cycle_node:
                break
        if not cycle_node:
            break
        # walk to ensure on cycle
        for _ in range(len(nodes)):
            cycle_node = parent[cycle_node]
        # cancel
        cycle = []
        v = cycle_node
        while True:
            cycle.append(v)
            v = parent[v]
            if v == cycle_node:
                break
        cycle.reverse()
        pf = min(residual[cycle[i]][cycle[(i+1)%len(cycle)]] for i in range(len(cycle)))
        for i in range(len(cycle)):
            u, w = cycle[i], cycle[(i+1)%len(cycle)]
            residual[u][w] -= pf
            residual[w][u] += pf
            cost_sum += pf * res_cost[u][w]
    return flow, cost_sum

if __name__ == "__main__":
    cap = {0: {1: 2, 2: 1}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    cst = {0: {1: 1, 2: 3}, 1: {3: 1}, 2: {3: 1}, 3: {}}
    f, c = cycle_canceling(cap, cst, 0, 3)
    assert abs(f - 2.0) < 1e-6
    print("cycle_canceling self-test passed", f, c)
