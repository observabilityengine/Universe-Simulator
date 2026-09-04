"""
Universe Simulator - k-Nearest Neighbors Classifier
Original pure-Python Euclidean k-NN.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import List, Tuple

class KNN:
    def __init__(self, k: int = 3):
        self.k = k
        self.data: List[Tuple[List[float], int]] = []

    def fit(self, X: List[List[float]], y: List[int]) -> None:
        self.data = list(zip(X, y))

    def predict(self, x: List[float]) -> int:
        dists = []
        for xi, yi in self.data:
            d = math.sqrt(sum((a - b) ** 2 for a, b in zip(x, xi)))
            dists.append((d, yi))
        dists.sort()
        votes = [yi for _, yi in dists[:self.k]]
        return Counter(votes).most_common(1)[0][0]

if __name__ == "__main__":
    X = [[0, 0], [0.1, 0.1], [1, 1], [1.1, 0.9], [0, 1], [1, 0]]
    y = [0, 0, 1, 1, 0, 1]
    clf = KNN(k=3)
    clf.fit(X, y)
    assert clf.predict([0.05, 0.05]) == 0
    assert clf.predict([1.05, 1.0]) == 1
    print("knn self-test passed")
