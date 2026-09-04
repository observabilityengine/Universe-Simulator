"""
Universe Simulator - Capacity-Scaled Dinic
Original Dinic with capacity scaling for better practical performance.
"""

from __future__ import annotations

from collections import deque
from typing import Dict

def dinic_scaling(capacity: Dict[int, Dict[int, float]], source: int, sink: int) -> float:
    residual = {u: dict(vs) for u, vs in capacity.items()}
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
            residual[v].setdefault(u, 0.0)
    max_cap = max((c for u in residual for c in residual[u].values()), default=0.0)
    delta = 1.0
    while delta * 2 <= max_cap:
        delta *= 2
    flow = 0.0
    while delta >= 1.0:
        while True:
            level = {source: 0}
            q = deque([source])
            while q:
                u = q.popleft()
                for v, cap in residual.get(u, {}).items():
                    if v not in level and cap >= delta:
                        level[v] = level[u] + 1
                        q.append(v)
            if sink not in level:
                break
            it = {u: 0 for u in residual}
            def dfs(u: int, pushed: float) -> float:
                if u == sink:
                    return pushed
                edges = list(residual.get(u, {}).items())
                while it[u] < len(edges):
                    v, cap = edges[it[u]]
                    if level.get(v, -1) == level[u] + 1 and cap >= delta:
                        tr = dfs(v, min(pushed, cap))
                        if tr > 0:
                            residual[u][v] -= tr
                            residual[v][u] += tr
                            return tr
                    it[u] += 1
                return 0.0
            while True:
                pushed = dfs(source, float("inf"))
                if pushed < 1e-12:
                    break
                flow += pushed
        delta /= 2
    return flow

if __name__ == "__main__":
    cap = {0: {1: 10, 2: 5}, 1: {2: 15, 3: 5}, 2: {3: 10}, 3: {}}
    assert abs(dinic_scaling(cap, 0, 3) - 15.0) < 1e-6
    print("dinic_scaling self-test passed")
