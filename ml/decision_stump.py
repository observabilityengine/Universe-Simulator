"""
Universe Simulator - Decision Stump (1-level decision tree)
Original axis-aligned threshold classifier.
"""

from __future__ import annotations

from typing import List, Tuple

class DecisionStump:
    def __init__(self) -> None:
        self.feature = 0
        self.threshold = 0.0
        self.polarity = 1  # 1 or -1

    def train(self, X: List[List[float]], y: List[int]) -> None:
        n, d = len(X), len(X[0])
        best_err = float("inf")
        for f in range(d):
            values = sorted(set(x[f] for x in X))
            for t in values:
                for pol in (1, -1):
                    err = 0
                    for i, x in enumerate(X):
                        pred = 1 if (x[f] >= t) == (pol == 1) else -1
                        if pred != y[i]:
                            err += 1
                    if err < best_err:
                        best_err = err
                        self.feature = f
                        self.threshold = t
                        self.polarity = pol

    def predict(self, x: List[float]) -> int:
        return 1 if (x[self.feature] >= self.threshold) == (self.polarity == 1) else -1

if __name__ == "__main__":
    X = [[0.1], [0.2], [0.8], [0.9]]
    y = [-1, -1, 1, 1]
    stump = DecisionStump()
    stump.train(X, y)
    assert stump.predict([0.15]) == -1 and stump.predict([0.85]) == 1
    print("decision_stump self-test passed")
