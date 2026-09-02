"""
Universe Simulator - Single-layer Perceptron
Original binary classifier with hard threshold.
"""

from __future__ import annotations

from typing import List, Tuple


class Perceptron:
    def __init__(self, dim: int, lr: float = 0.1):
        self.w = [0.0] * dim
        self.b = 0.0
        self.lr = lr

    def predict(self, x: List[float]) -> int:
        s = self.b + sum(wi * xi for wi, xi in zip(self.w, x))
        return 1 if s >= 0 else 0

    def train(self, data: List[Tuple[List[float], int]], epochs: int = 20) -> None:
        for _ in range(epochs):
            for x, y in data:
                pred = self.predict(x)
                err = y - pred
                for i in range(len(self.w)):
                    self.w[i] += self.lr * err * x[i]
                self.b += self.lr * err


if __name__ == "__main__":
    # AND gate
    data = [
        ([0.0, 0.0], 0),
        ([0.0, 1.0], 0),
        ([1.0, 0.0], 0),
        ([1.0, 1.0], 1),
    ]
    p = Perceptron(2, lr=0.5)
    p.train(data, epochs=30)
    assert p.predict([1.0, 1.0]) == 1 and p.predict([0.0, 1.0]) == 0
    print("perceptron self-test passed", p.w, p.b)
