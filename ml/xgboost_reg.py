"""
Universe Simulator - Gradient Boosted Regression Trees (simplified XGBoost-style)
Original residual fitting with squared loss.
"""

from __future__ import annotations

from typing import List
from ml.decision_stump import DecisionStump

class XGBRegressor:
    def __init__(self, n_estimators: int = 10, lr: float = 0.1):
        self.n_estimators = n_estimators
        self.lr = lr
        self.trees: List[DecisionStump] = []
        self.base = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.base = sum(y) / len(y)
        residual = [yi - self.base for yi in y]
        self.trees = []
        for _ in range(self.n_estimators):
            labels = [1 if r >= 0 else -1 for r in residual]
            stump = DecisionStump()
            stump.train(X, labels)
            self.trees.append(stump)
            for i, x in enumerate(X):
                residual[i] -= self.lr * stump.predict(x)

    def predict(self, x: List[float]) -> float:
        pred = self.base
        for t in self.trees:
            pred += self.lr * t.predict(x)
        return pred

if __name__ == "__main__":
    X = [[0.0], [1.0], [2.0], [3.0], [4.0]]
    y = [0.0, 1.0, 4.0, 9.0, 16.0]
    model = XGBRegressor(n_estimators=8)
    model.fit(X, y)
    assert abs(model.predict([2.0]) - 4.0) < 3.0
    print("xgboost_reg self-test passed")
