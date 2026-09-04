"""
Universe Simulator - DBSCAN Clustering
Original density-based clustering.
"""

from __future__ import annotations

import math
from typing import List, Set

class DBSCAN:
    def __init__(self, eps: float = 0.5, min_samples: int = 3):
        self.eps = eps
        self.min_samples = min_samples
        self.labels_: List[int] = []

    def fit(self, X: List[List[float]]) -> None:
        n = len(X)
        self.labels_ = [-1] * n
        cluster_id = 0
        visited: Set[int] = set()

        def region_query(i: int) -> List[int]:
            return [j for j in range(n) if math.sqrt(sum((a-b)**2 for a,b in zip(X[i], X[j]))) <= self.eps]

        for i in range(n):
            if i in visited:
                continue
            visited.add(i)
            neighbors = region_query(i)
            if len(neighbors) < self.min_samples:
                self.labels_[i] = -1  # noise
                continue
            self.labels_[i] = cluster_id
            seeds = neighbors[:]
            k = 0
            while k < len(seeds):
                j = seeds[k]
                if j not in visited:
                    visited.add(j)
                    j_neighbors = region_query(j)
                    if len(j_neighbors) >= self.min_samples:
                        seeds.extend(j_neighbors)
                if self.labels_[j] == -1:
                    self.labels_[j] = cluster_id
                k += 1
            cluster_id += 1

if __name__ == "__main__":
    X = [[0, 0], [0.1, 0.1], [0.2, 0], [5, 5], [5.1, 5.1], [5.2, 5], [10, 10]]
    db = DBSCAN(eps=0.5, min_samples=2)
    db.fit(X)
    assert db.labels_[0] == db.labels_[1]
    assert db.labels_[0] != db.labels_[3]
    print("dbscan self-test passed", db.labels_)
