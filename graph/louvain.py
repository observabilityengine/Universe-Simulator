"""Louvain method for community detection.

Complexity: O(n log n) typical. Original implementation.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple
import random


def louvain(
    edges: List[Tuple[int, int, float]],
    n: int | None = None,
    resolution: float = 1.0,
) -> Dict[int, int]:
    """Detect communities with the Louvain algorithm. Returns node -> community_id."""
    if not edges:
        return {}
    if n is None:
        n = max(max(u, v) for u, v, _ in edges) + 1

    adj: Dict[int, Dict[int, float]] = defaultdict(lambda: defaultdict(float))
    for u, v, w in edges:
        if u == v:
            continue
        adj[u][v] += w
        adj[v][u] += w

    nodes = list(range(n))
    community = {i: i for i in nodes}
    k = {i: sum(adj[i].values()) for i in nodes}
    m = sum(k.values()) / 2.0
    if m == 0:
        return community

    def modularity_gain(node: int, target_comm: int, comm_tot: Dict[int, float]) -> float:
        ki = k[node]
        ki_in = sum(w for nei, w in adj[node].items() if community[nei] == target_comm)
        sigma_tot = comm_tot[target_comm]
        return ki_in - resolution * sigma_tot * ki / (2 * m)

    improved = True
    while improved:
        improved = False
        comm_tot: Dict[int, float] = defaultdict(float)
        for node in nodes:
            comm_tot[community[node]] += k[node]

        order = nodes[:]
        random.Random(42).shuffle(order)

        for node in order:
            cur_comm = community[node]
            comm_tot[cur_comm] -= k[node]
            best_comm = cur_comm
            best_gain = 0.0
            candidates = {community[nei] for nei in adj[node]}
            candidates.add(cur_comm)
            for c in candidates:
                gain = modularity_gain(node, c, comm_tot)
                if gain > best_gain:
                    best_gain = gain
                    best_comm = c
            community[node] = best_comm
            comm_tot[best_comm] += k[node]
            if best_comm != cur_comm:
                improved = True

    remap: Dict[int, int] = {}
    for node in nodes:
        c = community[node]
        if c not in remap:
            remap[c] = len(remap)
        community[node] = remap[c]
    return community


if __name__ == "__main__":
    edges = [
        (0, 1, 1.0), (1, 2, 1.0), (0, 2, 1.0),
        (3, 4, 1.0), (4, 5, 1.0), (3, 5, 1.0),
        (2, 3, 0.1),
    ]
    comm = louvain(edges, n=6)
    assert comm[0] == comm[1] == comm[2]
    assert comm[3] == comm[4] == comm[5]
    assert comm[0] != comm[3]
    print("louvain self-tests passed")
