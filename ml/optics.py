"""
Universe Simulator - OPTICS Clustering (simplified)
Original ordering points to identify clustering structure.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

class OPTICS:
    def __init__(self, min_samples: int = 3, max_eps: float = 1.0):
        self.min_samples = min_samples
        self.max_eps = max_eps
        self.ordering_: List[int] = []
        self.reachability_: List[float] = []

    def fit(self, X: List[List[float]]) -> None:
        n = len(X)
        processed = [False] * n
        reach = [float("inf")] * n
        self.ordering_ = []
        self.reachability_ = []

        def dist(i: int, j: int) -> float:
            return math.sqrt(sum((a-b)**2 for a,b in zip(X[i], X[j])))

        for i in range(n):
            if processed[i]:
                continue
            processed[i] = True
            self.ordering_.append(i)
            self.reachability_.append(reach[i] if reach[i] < float("inf") else self.max_eps)
            neighbors = [(j, dist(i, j)) for j in range(n) if not processed[j] and dist(i, j) <= self.max_eps]
            if len(neighbors) + 1 < self.min_samples:
                continue
            neighbors.sort(key=lambda x: x[1])
            seeds = neighbors[:]
            while seeds:
                seeds.sort(key=lambda x: x[1])
                j, d = seeds.pop(0)
                if processed[j]:
                    continue
                processed[j] = True
                self.ordering_.append(j)
                self.reachability_.append(d)
                j_neighbors = [(k, dist(j, k)) for k in range(n) if not processed[k] and dist(j, k) <= self.max_eps]
                if len(j_neighbors) + 1 >= self.min_samples:
                    for k, dk in j_neighbors:
                        if dk < reach[k]:
                            reach[k] = dk
                            seeds.append((k, dk))

if __name__ == "__main__":
    X = [[0,0],[0.1,0],[0.2,0.1],[5,5],[5.1,5],[5.2,5.1]]
    opt = OPTICS(min_samples=2, max_eps=1.0)
    opt.fit(X)
    assert len(opt.ordering_) == 6
    print("optics self-test passed", opt.ordering_)
