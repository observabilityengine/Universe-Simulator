"""K-means clustering with K-means++ initialization.

Complexity: O(iters * k * n * d). Original implementation.
"""
from __future__ import annotations
import random
from typing import List, Tuple

def kmeans(
    X: List[List[float]],
    k: int,
    max_iter: int = 100,
    seed: int = 42,
) -> Tuple[List[List[float]], List[int]]:
    rng = random.Random(seed)
    n, d = len(X), len(X[0])
    centroids = [X[rng.randrange(n)][:]]
    for _ in range(1, k):
        dists = []
        for x in X:
            md = min(sum((x[j]-c[j])**2 for j in range(d)) for c in centroids)
            dists.append(md)
        total = sum(dists)
        r = rng.random() * total
        cum = 0.0
        for i, dist in enumerate(dists):
            cum += dist
            if cum >= r:
                centroids.append(X[i][:])
                break
    labels = [0] * n
    for _ in range(max_iter):
        changed = False
        for i, x in enumerate(X):
            best = min(range(k), key=lambda c: sum((x[j]-centroids[c][j])**2 for j in range(d)))
            if labels[i] != best:
                labels[i] = best
                changed = True
        if not changed:
            break
        for c in range(k):
            members = [X[i] for i in range(n) if labels[i] == c]
            if members:
                centroids[c] = [sum(m[j] for m in members)/len(members) for j in range(d)]
    return centroids, labels

if __name__ == "__main__":
    X = [[0.0, 0.0], [0.1, 0.1], [5.0, 5.0], [5.1, 5.2], [0.2, 0.0], [4.9, 5.0]]
    cents, labs = kmeans(X, k=2, seed=1)
    assert len(set(labs)) == 2
    assert labs[0] == labs[1] == labs[4]
    assert labs[2] == labs[3] == labs[5]
    print("kmeans self-tests passed")
