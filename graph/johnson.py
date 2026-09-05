"""Johnson's all-pairs shortest paths (handles negative weights, no neg cycle).

Complexity: O(V^2 log V + V E) with Dijkstra + Bellman-Ford.
Adds potential reweighting. Nodes any hashable ints.
"""
from __future__ import annotations

from typing import Dict, List, Tuple
from graph.bellman_ford import bellman_ford, INF
from graph.dijkstra import dijkstra


def johnson(graph: Dict[int, List[Tuple[int, float]]]) -> Dict[int, Dict[int, float]]:
    """All-pairs distances. Raises if negative cycle."""
    nodes = set(graph.keys())
    for succs in graph.values():
        for v, _ in succs:
            nodes.add(v)
    if not nodes:
        return {}

    # Add super source
    q = max(nodes) + 1 if nodes else 0
    g_bf = {u: list(graph.get(u, [])) for u in nodes}
    g_bf[q] = [(v, 0.0) for v in nodes]

    dist_q, has_neg = bellman_ford(g_bf, q)
    if has_neg:
        raise ValueError("negative cycle detected")

    # Reweight
    h = dist_q
    g_re: Dict[int, List[Tuple[int, float]]] = {}
    for u in nodes:
        g_re[u] = []
        for v, w in graph.get(u, []):
            w_new = w + h[u] - h[v]
            g_re[u].append((v, w_new))

    # Dijkstra from each
    result: Dict[int, Dict[int, float]] = {}
    for u in nodes:
        d = dijkstra(g_re, u)
        result[u] = {}
        for v in nodes:
            if d.get(v, INF) < INF:
                result[u][v] = d[v] - h[u] + h[v]
            else:
                result[u][v] = INF
    return result


if __name__ == "__main__":
    g = {
        0: [(1, -2.0), (2, 4.0)],
        1: [(2, 3.0)],
        2: [],
    }
    dist = johnson(g)
    assert abs(dist[0][1] + 2.0) < 1e-9
    assert abs(dist[0][2] - 1.0) < 1e-9

    # No edges
    assert johnson({0: [], 1: []})[0][1] == INF

    # Neg cycle raises
    try:
        johnson({0: [(1, 1.0)], 1: [(0, -2.0)]})
        assert False
    except ValueError:
        pass

    print("johnson self-tests passed")
