"""
Universe Simulator - Random Forest (ensemble of decision stumps)
Original bagging + majority vote.
"""

from __future__ import annotations

import random
from typing import List, Tuple
from ml.decision_stump import DecisionStump

class RandomForest:
    def __init__(self, n_trees: int = 5, seed: int = 42):
        self.n_trees = n_trees
        self.rng = random.Random(seed)
        self.trees: List[DecisionStump] = []

    def fit(self, X: List[List[float]], y: List[int]) -> None:
        n = len(X)
        self.trees = []
        for _ in range(self.n_trees):
            idx = [self.rng.randint(0, n - 1) for _ in range(n)]
            Xb = [X[i] for i in idx]
            yb = [y[i] for i in idx]
            stump = DecisionStump()
            stump.train(Xb, yb)
            self.trees.append(stump)

    def predict(self, x: List[float]) -> int:
        votes = [t.predict(x) for t in self.trees]
        return max(set(votes), key=votes.count)

if __name__ == "__main__":
    X = [[0.1], [0.2], [0.8], [0.9], [0.15], [0.85]]
    y = [-1, -1, 1, 1, -1, 1]
    rf = RandomForest(n_trees=7)
    rf.fit(X, y)
    assert rf.predict([0.12]) == -1
    print("random_forest self-test passed")
