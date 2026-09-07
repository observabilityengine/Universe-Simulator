"""k-Nearest Neighbors classifier and regressor.

Complexity: O(n d) per query. Original implementation.
"""
from __future__ import annotations

from typing import List, Any
import math


def _dist(a: List[float], b: List[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


class KNNClassifier:
    def __init__(self, k: int = 3) -> None:
        self.k = k
        self.X: List[List[float]] = []
        self.y: List[Any] = []

    def fit(self, X: List[List[float]], y: List[Any]) -> "KNNClassifier":
        self.X, self.y = X, y
        return self

    def predict(self, X: List[List[float]]) -> List[Any]:
        preds = []
        for x in X:
            dists = [(_dist(x, self.X[i]), self.y[i]) for i in range(len(self.X))]
            dists.sort()
            votes: dict = {}
            for _, label in dists[: self.k]:
                votes[label] = votes.get(label, 0) + 1
            preds.append(max(votes, key=votes.get))
        return preds


class KNNRegressor:
    def __init__(self, k: int = 3) -> None:
        self.k = k
        self.X: List[List[float]] = []
        self.y: List[float] = []

    def fit(self, X: List[List[float]], y: List[float]) -> "KNNRegressor":
        self.X, self.y = X, y
        return self

    def predict(self, X: List[List[float]]) -> List[float]:
        preds = []
        for x in X:
            dists = [(_dist(x, self.X[i]), self.y[i]) for i in range(len(self.X))]
            dists.sort()
            preds.append(sum(v for _, v in dists[: self.k]) / self.k)
        return preds


if __name__ == "__main__":
    X = [[0, 0], [0, 1], [1, 0], [1, 1], [5, 5], [5, 6], [6, 5]]
    y = [0, 0, 0, 0, 1, 1, 1]
    clf = KNNClassifier(k=3).fit(X, y)
    assert clf.predict([[0.1, 0.1]])[0] == 0
    assert clf.predict([[5.5, 5.5]])[0] == 1
    reg = KNNRegressor(k=2).fit([[0], [1], [2], [3]], [0.0, 2.0, 4.0, 6.0])
    assert abs(reg.predict([[1.5]])[0] - 3.0) < 0.1
    print("knn self-tests passed")
