"""
Universe Simulator - Karger Min-Cut
Original randomized contraction algorithm.
"""

from __future__ import annotations

import random
from typing import Dict, List, Tuple

def karger_mincut(graph: Dict[int, List[int]], trials: int = 20, seed: int = 42) -> int:
    rng = random.Random(seed)
    best = float("inf")
    for _ in range(trials):
        # deep copy edges
        edges = []
        for u, vs in graph.items():
            for v in vs:
                if u < v:
                    edges.append((u, v))
        parent = {u: u for u in graph}
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        n = len(graph)
        while n > 2:
            if not edges:
                break
            e = edges[rng.randint(0, len(edges)-1)]
            u, v = find(e[0]), find(e[1])
            if u == v:
                edges = [x for x in edges if find(x[0]) != find(x[1])]
                continue
            parent[v] = u
            n -= 1
            edges = [(find(a), find(b)) for a, b in edges if find(a) != find(b)]
        cut = len(edges)
        if cut < best:
            best = cut
    return int(best)

if __name__ == "__main__":
    g = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2]}
    cut = karger_mincut(g)
    assert cut >= 1
    print("karger_mincut self-test passed", cut)
