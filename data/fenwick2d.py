"""
Universe Simulator - 2-D Fenwick Tree
Original point update + rectangle sum.
"""

from __future__ import annotations

from typing import List

class Fenwick2D:
    def __init__(self, rows: int, cols: int):
        self.r = rows
        self.c = cols
        self.bit = [[0.0] * (cols + 1) for _ in range(rows + 1)]

    def update(self, x: int, y: int, delta: float) -> None:
        i = x + 1
        while i <= self.r:
            j = y + 1
            while j <= self.c:
                self.bit[i][j] += delta
                j += j & -j
            i += i & -i

    def _prefix(self, x: int, y: int) -> float:
        s = 0.0
        i = x + 1
        while i > 0:
            j = y + 1
            while j > 0:
                s += self.bit[i][j]
                j -= j & -j
            i -= i & -i
        return s

    def range_sum(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return (self._prefix(x2, y2) - self._prefix(x1 - 1, y2)
                - self._prefix(x2, y1 - 1) + self._prefix(x1 - 1, y1 - 1))

if __name__ == "__main__":
    ft = Fenwick2D(4, 4)
    ft.update(1, 1, 5)
    ft.update(2, 2, 3)
    assert abs(ft.range_sum(0, 0, 3, 3) - 8) < 1e-9
    assert abs(ft.range_sum(1, 1, 1, 1) - 5) < 1e-9
    print("fenwick2d self-test passed")
