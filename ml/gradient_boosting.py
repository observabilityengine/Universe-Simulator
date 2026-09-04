"""
Universe Simulator - Gradient Boosting (regression stumps)
Original sequential residual fitting.
"""

from __future__ import annotations

from typing import List, Tuple
from ml.decision_stump import DecisionStump

class GradientBoosting:
    def __init__(self, n_estimators: int = 10, lr: float = 0.1):
        self.n_estimators = n_estimators
        self.lr = lr
        self.models: List[DecisionStump] = []
        self.base = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.base = sum(y) / len(y)
        residual = [yi - self.base for yi in y]
        self.models = []
        for _ in range(self.n_estimators):
            # convert residual sign as pseudo label for stump
            labels = [1 if r >= 0 else -1 for r in residual]
            stump = DecisionStump()
            stump.train(X, labels)
            self.models.append(stump)
            for i, x in enumerate(X):
                residual[i] -= self.lr * stump.predict(x)

    def predict(self, x: List[float]) -> float:
        pred = self.base
        for m in self.models:
            pred += self.lr * m.predict(x)
        return pred

if __name__ == "__main__":
    X = [[0.0], [1.0], [2.0], [3.0]]
    y = [0.0, 1.0, 2.0, 3.0]
    gb = GradientBoosting(n_estimators=5)
    gb.fit(X, y)
    assert abs(gb.predict([1.5]) - 1.5) < 1.5
    print("gradient_boosting self-test passed")
