"""
Universe Simulator - Logistic Regression (gradient descent)
Original binary classifier with sigmoid.
"""

from __future__ import annotations

import math
from typing import List, Tuple


def sigmoid(z: float) -> float:
    z = max(-500.0, min(500.0, z))
    return 1.0 / (1.0 + math.exp(-z))


class LogisticRegression:
    def __init__(self, dim: int, lr: float = 0.1):
        self.w = [0.0] * dim
        self.b = 0.0
        self.lr = lr

    def predict_proba(self, x: List[float]) -> float:
        return sigmoid(self.b + sum(wi * xi for wi, xi in zip(self.w, x)))

    def predict(self, x: List[float]) -> int:
        return 1 if self.predict_proba(x) >= 0.5 else 0

    def train(self, data: List[Tuple[List[float], int]], epochs: int = 200) -> None:
        for _ in range(epochs):
            for x, y in data:
                p = self.predict_proba(x)
                err = p - y
                for i in range(len(self.w)):
                    self.w[i] -= self.lr * err * x[i]
                self.b -= self.lr * err


if __name__ == "__main__":
    data = [
        ([0.0, 0.0], 0), ([0.1, 0.2], 0), ([0.9, 0.8], 1),
        ([1.0, 1.0], 1), ([0.2, 0.1], 0), ([0.8, 0.9], 1),
    ]
    model = LogisticRegression(2, lr=0.5)
    model.train(data, epochs=300)
    assert model.predict([0.0, 0.0]) == 0
    assert model.predict([1.0, 1.0]) == 1
    print("logistic self-test passed", model.w, model.b)
