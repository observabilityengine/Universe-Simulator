"""
Universe Simulator - Push-Relabel Max Flow
Original highest-label preflow-push.
"""

from __future__ import annotations

from typing import Dict, List

def push_relabel(capacity: Dict[int, Dict[int, float]], source: int, sink: int) -> float:
    nodes = set(capacity.keys())
    for u in capacity:
        nodes.update(capacity[u].keys())
    residual = {u: dict(vs) for u, vs in capacity.items()}
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
            residual[v].setdefault(u, 0.0)
    height = {u: 0 for u in nodes}
    excess = {u: 0.0 for u in nodes}
    height[source] = len(nodes)
    for v, cap in list(residual.get(source, {}).items()):
        residual[source][v] = 0.0
        residual[v][source] += cap
        excess[v] += cap

    def push(u: int, v: int) -> None:
        delta = min(excess[u], residual[u][v])
        residual[u][v] -= delta
        residual[v][u] += delta
        excess[u] -= delta
        excess[v] += delta

    def relabel(u: int) -> None:
        min_h = min(height[v] for v, cap in residual[u].items() if cap > 1e-12)
        height[u] = min_h + 1

    active = [u for u in nodes if u != source and u != sink and excess[u] > 1e-12]
    while active:
        u = active.pop()
        pushed = False
        for v, cap in list(residual.get(u, {}).items()):
            if cap > 1e-12 and height[u] == height[v] + 1:
                push(u, v)
                if v != source and v != sink and excess[v] > 1e-12 and v not in active:
                    active.append(v)
                pushed = True
                if excess[u] <= 1e-12:
                    break
        if excess[u] > 1e-12:
            relabel(u)
            active.append(u)
    return excess[sink]

if __name__ == "__main__":
    cap = {0: {1: 10, 2: 5}, 1: {2: 15, 3: 5}, 2: {3: 10}, 3: {}}
    assert abs(push_relabel(cap, 0, 3) - 15.0) < 1e-6
    print("push_relabel self-test passed")
