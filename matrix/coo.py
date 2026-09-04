"""
Universe Simulator - COO Sparse Matrix
Original coordinate format + conversion to dense.
"""

from __future__ import annotations

from typing import List, Tuple

class COOMatrix:
    def __init__(self, rows: List[int], cols: List[int], data: List[float], shape: Tuple[int, int]):
        self.rows = rows
        self.cols = cols
        self.data = data
        self.shape = shape

    def to_dense(self) -> List[List[float]]:
        m, n = self.shape
        dense = [[0.0] * n for _ in range(m)]
        for r, c, v in zip(self.rows, self.cols, self.data):
            dense[r][c] += v
        return dense

    def matvec(self, x: List[float]) -> List[float]:
        y = [0.0] * self.shape[0]
        for r, c, v in zip(self.rows, self.cols, self.data):
            y[r] += v * x[c]
        return y

if __name__ == "__main__":
    coo = COOMatrix([0, 0, 1, 2], [0, 2, 1, 0], [1.0, 2.0, 3.0, 4.0], (3, 3))
    dense = coo.to_dense()
    assert dense[0][0] == 1.0 and dense[1][1] == 3.0
    print("coo self-test passed", dense)
