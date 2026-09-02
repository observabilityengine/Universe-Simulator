"""
Universe Simulator - K-Means Clustering
Original pure-Python Lloyd iteration with random init.
"""

from __future__ import annotations

import random
import math
from typing import List, Tuple

Point = Tuple[float, ...]


def _dist2(a: Point, b: Point) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def kmeans(
    data: List[Point],
    k: int,
    max_iter: int = 100,
    seed: int = 42,
) -> Tuple[List[Point], List[int]]:
    if k <= 0 or k > len(data):
        raise ValueError("invalid k")
    rng = random.Random(seed)
    centroids = [data[i] for i in rng.sample(range(len(data)), k)]
    labels = [0] * len(data)

    for _ in range(max_iter):
        # assign
        changed = False
        for i, p in enumerate(data):
            best = min(range(k), key=lambda c: _dist2(p, centroids[c]))
            if labels[i] != best:
                labels[i] = best
                changed = True
        # update
        new_centroids: List[Point] = []
        for c in range(k):
            members = [data[i] for i, lab in enumerate(labels) if lab == c]
            if not members:
                new_centroids.append(centroids[c])
                continue
            dim = len(members[0])
            avg = tuple(sum(m[d] for m in members) / len(members) for d in range(dim))
            new_centroids.append(avg)
        centroids = new_centroids
        if not changed:
            break
    return centroids, labels


if __name__ == "__main__":
    pts = [(0.0, 0.0), (0.1, 0.1), (5.0, 5.0), (5.1, 5.2), (10.0, 0.0)]
    cents, labs = kmeans(pts, k=2, seed=1)
    print("kmeans self-test passed", cents, labs)
