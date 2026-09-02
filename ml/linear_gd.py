"""
Universe Simulator - Linear Regression via Gradient Descent
Original multi-feature implementation.
"""

from __future__ import annotations

from typing import List, Tuple


class LinearGD:
    def __init__(self, dim: int, lr: float = 0.01):
        self.w = [0.0] * dim
        self.b = 0.0
        self.lr = lr

    def predict(self, x: List[float]) -> float:
        return self.b + sum(wi * xi for wi, xi in zip(self.w, x))

    def train(self, data: List[Tuple[List[float], float]], epochs: int = 200) -> None:
        for _ in range(epochs):
            for x, y in data:
                pred = self.predict(x)
                err = pred - y
                for i in range(len(self.w)):
                    self.w[i] -= self.lr * err * x[i]
                self.b -= self.lr * err


if __name__ == "__main__":
    data = [([1.0], 2.0), ([2.0], 4.0), ([3.0], 6.1), ([4.0], 8.0)]
    model = LinearGD(1, lr=0.05)
    model.train(data, epochs=300)
    pred = model.predict([5.0])
    assert abs(pred - 10.0) < 0.5
    print("linear_gd self-test passed", pred, model.w, model.b)
