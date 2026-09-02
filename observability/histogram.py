"""
Universe Simulator - Streaming Histogram
Original fixed-bucket histogram for metrics.
"""

from __future__ import annotations

from typing import List, Tuple


class Histogram:
    def __init__(self, bounds: List[float]):
        """bounds are upper edges of buckets, must be sorted ascending."""
        self.bounds = sorted(bounds)
        self.counts = [0] * (len(self.bounds) + 1)  # +1 for overflow

    def observe(self, value: float) -> None:
        for i, b in enumerate(self.bounds):
            if value <= b:
                self.counts[i] += 1
                return
        self.counts[-1] += 1

    def total(self) -> int:
        return sum(self.counts)

    def buckets(self) -> List[Tuple[str, int]]:
        labels = []
        prev = float("-inf")
        for b in self.bounds:
            labels.append(f"({prev}, {b}]")
            prev = b
        labels.append(f"({prev}, +inf)")
        return list(zip(labels, self.counts))


if __name__ == "__main__":
    h = Histogram([0.1, 0.5, 1.0, 5.0])
    for v in [0.05, 0.2, 0.7, 2.0, 10.0, 0.3]:
        h.observe(v)
    assert h.total() == 6
    assert h.counts[0] == 1  # <=0.1
    print("histogram self-test passed", h.buckets())
