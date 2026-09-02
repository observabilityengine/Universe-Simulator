"""
Universe Simulator - Sparse Table for RMQ (Range Minimum Query)
Original O(n log n) build, O(1) query.
"""

from __future__ import annotations

import math
from typing import List


class SparseTable:
    def __init__(self, data: List[float]):
        self.n = len(data)
        if self.n == 0:
            self.st = []
            return
        self.log = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1
        k = self.log[self.n] + 1
        self.st = [[0.0] * self.n for _ in range(k)]
        self.st[0] = data[:]
        for j in range(1, k):
            for i in range(self.n - (1 << j) + 1):
                self.st[j][i] = min(self.st[j-1][i], self.st[j-1][i + (1 << (j-1))])

    def query(self, left: int, right: int) -> float:
        if left > right or left < 0 or right >= self.n:
            raise ValueError("invalid range")
        j = self.log[right - left + 1]
        return min(self.st[j][left], self.st[j][right - (1 << j) + 1])


if __name__ == "__main__":
    st = SparseTable([4.0, 2.0, 7.0, 1.0, 9.0, 3.0])
    assert st.query(0, 5) == 1.0
    assert st.query(2, 4) == 1.0
    assert st.query(0, 1) == 2.0
    print("sparse_table self-test passed")
