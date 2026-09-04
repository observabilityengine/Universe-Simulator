"""
Universe Simulator - Stoer-Wagner Min-Cut
Original deterministic global min-cut for undirected graphs.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

def stoer_wagner(graph: Dict[int, Dict[int, float]]) -> float:
    """graph is undirected weighted adjacency."""
    vertices = set(graph.keys())
    for u in graph:
        for v in graph[u]:
            vertices.add(v)
    best = float("inf")
    while len(vertices) > 1:
        # maximum adjacency search
        a = next(iter(vertices))
        found = {a}
        weights = {v: graph.get(a, {}).get(v, 0.0) for v in vertices if v != a}
        order = [a]
        while len(found) < len(vertices):
            next_v = max((v for v in vertices if v not in found), key=lambda x: weights.get(x, 0.0))
            found.add(next_v)
            order.append(next_v)
            for v in vertices:
                if v not in found:
                    weights[v] = weights.get(v, 0.0) + graph.get(next_v, {}).get(v, 0.0)
        s, t = order[-2], order[-1]
        cut = weights.get(t, 0.0)
        if cut < best:
            best = cut
        # merge s and t
        if s not in graph:
            graph[s] = {}
        for v, w in graph.get(t, {}).items():
            if v != s:
                graph[s][v] = graph[s].get(v, 0.0) + w
                graph.setdefault(v, {})[s] = graph[s][v]
        for v in list(graph.keys()):
            if t in graph[v]:
                del graph[v][t]
        if t in graph:
            del graph[t]
        vertices.remove(t)
    return best

if __name__ == "__main__":
    g = {0: {1: 2.0, 2: 3.0}, 1: {0: 2.0, 2: 1.0, 3: 4.0}, 2: {0: 3.0, 1: 1.0, 3: 2.0}, 3: {1: 4.0, 2: 2.0}}
    cut = stoer_wagner(g)
    assert cut > 0
    print("stoer_wagner self-test passed", cut)
