"""Gradient Boosting for regression (squared loss) with decision stumps.

Complexity: O(n_estimators * n_samples * features). Original implementation.
"""
from __future__ import annotations
from typing import List, Tuple

def _best_stump(X: List[List[float]], residuals: List[float]) -> Tuple[int, float, float, float]:
    n, d = len(X), len(X[0])
    best_loss = float("inf")
    best = (0, 0.0, 0.0, 0.0)
    for f in range(d):
        vals = sorted(set(row[f] for row in X))
        for i in range(len(vals) - 1):
            thr = (vals[i] + vals[i + 1]) / 2
            left_r = [residuals[j] for j in range(n) if X[j][f] <= thr]
            right_r = [residuals[j] for j in range(n) if X[j][f] > thr]
            if not left_r or not right_r:
                continue
            left_val = sum(left_r) / len(left_r)
            right_val = sum(right_r) / len(right_r)
            loss = sum((r - left_val) ** 2 for r in left_r) + sum((r - right_val) ** 2 for r in right_r)
            if loss < best_loss:
                best_loss = loss
                best = (f, thr, left_val, right_val)
    return best

class GradientBoostingRegressor:
    def __init__(self, n_estimators: int = 50, learning_rate: float = 0.1) -> None:
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.stumps: List[Tuple[int, float, float, float]] = []
        self.base_prediction = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> "GradientBoostingRegressor":
        n = len(y)
        self.base_prediction = sum(y) / n
        pred = [self.base_prediction] * n
        self.stumps = []
        for _ in range(self.n_estimators):
            residuals = [y[i] - pred[i] for i in range(n)]
            stump = _best_stump(X, residuals)
            self.stumps.append(stump)
            f, thr, lv, rv = stump
            for i in range(n):
                pred[i] += self.learning_rate * (lv if X[i][f] <= thr else rv)
        return self

    def predict(self, X: List[List[float]]) -> List[float]:
        preds = [self.base_prediction] * len(X)
        for f, thr, lv, rv in self.stumps:
            for i, row in enumerate(X):
                preds[i] += self.learning_rate * (lv if row[f] <= thr else rv)
        return preds

if __name__ == "__main__":
    X = [[float(i), float(j)] for i in range(5) for j in range(5)]
    y = [2 * x[0] - x[1] + 0.01 * (i % 3) for i, x in enumerate(X)]
    gbr = GradientBoostingRegressor(n_estimators=40, learning_rate=0.15).fit(X, y)
    preds = gbr.predict(X)
    mse = sum((p - t) ** 2 for p, t in zip(preds, y)) / len(y)
    assert mse < 1.0, mse
    print("gradient_boosting self-tests passed")
