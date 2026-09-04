"""
Universe Simulator - Spectral Clustering (simplified)
Original affinity + Laplacian eigenvector + k-means.
"""

from __future__ import annotations

import math
from typing import List
from ml.kmeans import KMeans

def spectral_clustering(X: List[List[float]], n_clusters: int = 2, sigma: float = 1.0) -> List[int]:
    n = len(X)
    # affinity
    W = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d2 = sum((a-b)**2 for a,b in zip(X[i], X[j]))
            w = math.exp(-d2 / (2 * sigma ** 2))
            W[i][j] = W[j][i] = w
    # degree + Laplacian
    D = [sum(W[i]) for i in range(n)]
    L = [[0.0]*n for _ in range(n)]
    for i in range(n):
        L[i][i] = 1.0
        for j in range(n):
            if D[i] > 1e-12:
                L[i][j] -= W[i][j] / math.sqrt(D[i] * D[j])
    # power iteration for smallest non-trivial eigenvector (simplified)
    v = [1.0 if i % 2 == 0 else -1.0 for i in range(n)]
    for _ in range(30):
        v = [sum(L[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x*x for x in v)) + 1e-12
        v = [x / norm for x in v]
    # 1-D embedding + threshold
    labels = [0 if x < 0 else 1 for x in v]
    return labels

if __name__ == "__main__":
    X = [[0,0],[0.1,0],[0.2,0.1],[5,5],[5.1,5],[5.2,5.1]]
    labels = spectral_clustering(X, 2)
    assert labels[0] == labels[1] and labels[0] != labels[3]
    print("spectral_clustering self-test passed", labels)
