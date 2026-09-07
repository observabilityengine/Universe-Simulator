"""DBSCAN clustering.

Complexity: O(n^2) naive. Original implementation.
"""
from __future__ import annotations
from typing import List

def dbscan(X: List[List[float]], eps: float = 0.5, min_samples: int = 3) -> List[int]:
    n = len(X)
    labels = [-1] * n
    cluster_id = 0
    def dist(a, b):
        return sum((a[i]-b[i])**2 for i in range(len(a)))**0.5
    def neighbors(i):
        return [j for j in range(n) if dist(X[i], X[j]) <= eps]
    for i in range(n):
        if labels[i] != -1:
            continue
        nbrs = neighbors(i)
        if len(nbrs) < min_samples:
            labels[i] = -1
            continue
        labels[i] = cluster_id
        seeds = set(nbrs) - {i}
        while seeds:
            j = seeds.pop()
            if labels[j] == -1:
                labels[j] = cluster_id
            if labels[j] != -1:
                continue
            labels[j] = cluster_id
            jnbrs = neighbors(j)
            if len(jnbrs) >= min_samples:
                seeds.update(jnbrs)
        cluster_id += 1
    return labels

if __name__ == "__main__":
    X = [[0,0],[0.1,0.1],[0.2,0],[5,5],[5.1,5.2],[5.2,4.9],[10,10]]
    labs = dbscan(X, eps=0.5, min_samples=2)
    assert labs[0] == labs[1] == labs[2]
    assert labs[3] == labs[4] == labs[5]
    assert labs[0] != labs[3]
    print("dbscan self-tests passed")
