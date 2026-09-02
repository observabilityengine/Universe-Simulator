"""
Universe Simulator - Fenwick Tree (Binary Indexed Tree)
Original point-update / prefix-sum structure.
"""

from __future__ import annotations

from typing import List


class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0.0] * (n + 1)

    def update(self, i: int, delta: float) -> None:
        i += 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix(self, i: int) -> float:
        i += 1
        s = 0.0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, left: int, right: int) -> float:
        if left == 0:
            return self.prefix(right)
        return self.prefix(right) - self.prefix(left - 1)


if __name__ == "__main__":
    ft = FenwickTree(8)
    for i, v in enumerate([1, 3, 5, 7, 9, 11, 13, 15]):
        ft.update(i, v)
    assert abs(ft.range_sum(2, 5) - (5+7+9+11)) < 1e-9
    ft.update(3, 10)
    assert abs(ft.prefix(3) - (1+3+5+17)) < 1e-9
    print("fenwick self-test passed")
