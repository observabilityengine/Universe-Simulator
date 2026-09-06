"""Welford's online algorithm for mean and variance.

Complexity: O(1) update, O(1) space.
Numerically stable single-pass running mean/variance.
Original implementation.
"""
from __future__ import annotations


class WelfordVariance:
    """Online mean and sample/population variance."""

    def __init__(self) -> None:
        self.n = 0
        self.mean = 0.0
        self.m2 = 0.0

    def update(self, x: float) -> None:
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        delta2 = x - self.mean
        self.m2 += delta * delta2

    def variance(self, sample: bool = True) -> float:
        if self.n < 2:
            return 0.0
        return self.m2 / (self.n - 1) if sample else self.m2 / self.n

    def std(self, sample: bool = True) -> float:
        return self.variance(sample) ** 0.5


if __name__ == "__main__":
    w = WelfordVariance()
    for x in [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]:
        w.update(x)
    assert abs(w.mean - 5.0) < 1e-12
    assert abs(w.variance(sample=True) - 4.57142857) < 1e-6
    w2 = WelfordVariance()
    w2.update(10.0)
    assert w2.variance() == 0.0
    assert WelfordVariance().variance() == 0.0
    print("welford_variance self-tests passed")
