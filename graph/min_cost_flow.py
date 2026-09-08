"""Successive shortest path minimum-cost maximum-flow with potentials (Dijkstra).

Complexity: O(F * (E + V) log V). Original implementation.
"""
from __future__ import annotations
import heapq
from typing import List, Tuple, Dict


def min_cost_max_flow(
    n: int,
    edges: List[Tuple[int, int, int, int]],
    source: int,
    sink: int,
) -> Tuple[int, int]:
    """edges = (u, v, capacity, cost). Returns (max_flow, min_cost)."""
    graph: List[List[List[int]]] = [[] for _ in range(n)]  # to, cap, cost, rev
    for u, v, cap, cost in edges:
        graph[u].append([v, cap, cost, len(graph[v])])
        graph[v].append([u, 0, -cost, len(graph[u]) - 1])

    flow = cost = 0
    potential = [0] * n

    while True:
        dist = [float("inf")] * n
        dist[source] = 0
        parent: List[Tuple[int, int]] = [(-1, -1)] * n  # (node, edge_idx)
        pq = [(0, source)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for i, e in enumerate(graph[u]):
                v, cap, c, _ = e
                if cap <= 0:
                    continue
                nd = dist[u] + c + potential[u] - potential[v]
                if nd < dist[v]:
                    dist[v] = nd
                    parent[v] = (u, i)
                    heapq.heappush(pq, (nd, v))
        if dist[sink] == float("inf"):
            break
        for i in range(n):
            if dist[i] < float("inf"):
                potential[i] += dist[i]
        # Augment
        aug = float("inf")
        v = sink
        while v != source:
            u, ei = parent[v]
            aug = min(aug, graph[u][ei][1])
            v = u
        v = sink
        while v != source:
            u, ei = parent[v]
            graph[u][ei][1] -= aug
            rev = graph[u][ei][3]
            graph[v][rev][1] += aug
            cost += aug * graph[u][ei][2]
            v = u
        flow += aug
    return flow, cost


if __name__ == "__main__":
    edges = [
        (0, 1, 5, 2),
        (0, 2, 3, 4),
        (1, 2, 2, 1),
        (1, 3, 4, 3),
        (2, 3, 6, 2),
    ]
    f, c = min_cost_max_flow(4, edges, 0, 3)
    assert f == 8, f
    assert c > 0
    print(f"min_cost_flow flow={f} cost={c}")
    print("min_cost_flow self-tests passed")
