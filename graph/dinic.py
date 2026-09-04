"""
Universe Simulator - Dinic Max Flow
Original level-graph + DFS blocking flow.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List

def dinic(capacity: Dict[int, Dict[int, float]], source: int, sink: int) -> float:
    residual = {u: dict(vs) for u, vs in capacity.items()}
    for u in list(residual):
        for v in residual[u]:
            residual.setdefault(v, {})
            residual[v].setdefault(u, 0.0)

    def bfs_level() -> Dict[int, int]:
        level = {source: 0}
        q = deque([source])
        while q:
            u = q.popleft()
            for v, cap in residual.get(u, {}).items():
                if v not in level and cap > 1e-12:
                    level[v] = level[u] + 1
                    q.append(v)
        return level

    def dfs(u: int, pushed: float, level: Dict[int, int], it: Dict[int, int]) -> float:
        if u == sink:
            return pushed
        edges = list(residual.get(u, {}).items())
        while it[u] < len(edges):
            v, cap = edges[it[u]]
            if level.get(v, -1) == level[u] + 1 and cap > 1e-12:
                tr = dfs(v, min(pushed, cap), level, it)
                if tr > 1e-12:
                    residual[u][v] -= tr
                    residual[v][u] += tr
                    return tr
            it[u] += 1
        return 0.0

    flow = 0.0
    while True:
        level = bfs_level()
        if sink not in level:
            break
        it = {u: 0 for u in residual}
        while True:
            pushed = dfs(source, float("inf"), level, it)
            if pushed < 1e-12:
                break
            flow += pushed
    return flow

if __name__ == "__main__":
    cap = {0: {1: 10, 2: 5}, 1: {2: 15, 3: 5}, 2: {3: 10}, 3: {}}
    assert abs(dinic(cap, 0, 3) - 15.0) < 1e-6
    print("dinic self-test passed")
