"""
Universe Simulator - Capacity Scaling Max Flow
Original successive doubling of capacity threshold.
"""

from __future__ import annotations

from collections import deque
from typing import Dict

def capacity_scaling(capacity: Dict[int, Dict[int, float]], source: int, sink: int) -> float:
    residual = {u: dict(vs) for u, vs in capacity.items()}
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
            residual[v].setdefault(u, 0.0)
    max_cap = max((c for u in residual for c in residual[u].values()), default=0)
    delta = 1
    while delta * 2 <= max_cap:
        delta *= 2
    flow = 0.0
    while delta >= 1:
        while True:
            parent = {}
            q = deque([source])
            parent[source] = None
            found = False
            while q and not found:
                u = q.popleft()
                for v, cap in residual.get(u, {}).items():
                    if v not in parent and cap >= delta:
                        parent[v] = u
                        if v == sink:
                            found = True
                            break
                        q.append(v)
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
        delta //= 2
    return flow

if __name__ == "__main__":
    cap = {0: {1: 10, 2: 5}, 1: {2: 15, 3: 5}, 2: {3: 10}, 3: {}}
    assert abs(capacity_scaling(cap, 0, 3) - 15.0) < 1e-6
    print("capacity_scaling self-test passed")
