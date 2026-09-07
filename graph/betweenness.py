"""Brandes' algorithm for betweenness centrality.

Complexity: O(V E) for unweighted graphs. Original implementation.
"""
from __future__ import annotations

from collections import deque
from typing import Dict, List, Tuple


def betweenness_centrality(
    n: int,
    edges: List[Tuple[int, int]],
) -> List[float]:
    """
    Compute betweenness centrality for an undirected unweighted graph.
    Returns list of centrality scores, one per node.
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    cb = [0.0] * n
    for s in range(n):
        stack: List[int] = []
        pred: List[List[int]] = [[] for _ in range(n)]
        sigma = [0] * n
        sigma[s] = 1
        dist = [-1] * n
        dist[s] = 0
        q: deque[int] = deque([s])
        while q:
            v = q.popleft()
            stack.append(v)
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    q.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = [0.0] * n
        while stack:
            w = stack.pop()
            for v in pred[w]:
                if sigma[w] > 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                cb[w] += delta[w]
    return [c / 2.0 for c in cb]


if __name__ == "__main__":
    edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    bc = betweenness_centrality(5, edges)
    assert bc[2] > bc[1] > bc[0]
    assert bc[0] == 0.0
    star = [(0, 1), (0, 2), (0, 3), (0, 4)]
    bc2 = betweenness_centrality(5, star)
    assert bc2[0] > bc2[1]
    print("betweenness self-tests passed")
