"""
Universe Simulator - Fenwick Tree for Range Minimum
Original point update + prefix minimum.
"""

from __future__ import annotations

from typing import List

class FenwickMin:
    def __init__(self, n: int):
        self.n = n
        self.bit = [float("inf")] * (n + 1)

    def update(self, i: int, val: float) -> None:
        i += 1
        while i <= self.n:
            self.bit[i] = min(self.bit[i], val)
            i += i & -i

    def prefix_min(self, i: int) -> float:
        i += 1
        res = float("inf")
        while i > 0:
            res = min(res, self.bit[i])
            i -= i & -i
        return res

if __name__ == "__main__":
    ft = FenwickMin(8)
    for i, v in enumerate([5, 3, 7, 1, 9, 2, 8, 4]):
        ft.update(i, v)
    assert ft.prefix_min(3) == 1.0
    assert ft.prefix_min(0) == 5.0
    print("fenwick_min self-test passed")
