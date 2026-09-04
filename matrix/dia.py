"""
Universe Simulator - DIA (Diagonal) Sparse Matrix
Original diagonal storage + matvec.
"""

from __future__ import annotations

from typing import List, Tuple

class DIAMatrix:
    def __init__(self, data: List[List[float]], offsets: List[int], shape: Tuple[int, int]):
        self.data = data
        self.offsets = offsets
        self.shape = shape

    @classmethod
    def from_dense(cls, dense: List[List[float]]) -> "DIAMatrix":
        m = len(dense)
        n = len(dense[0]) if dense else 0
        offsets_set = set()
        for i in range(m):
            for j in range(n):
                if abs(dense[i][j]) > 1e-15:
                    offsets_set.add(j - i)
        offsets = sorted(offsets_set)
        data = [[0.0]*m for _ in offsets]
        for k, off in enumerate(offsets):
            for i in range(m):
                j = i + off
                if 0 <= j < n:
                    data[k][i] = dense[i][j]
        return cls(data, offsets, (m, n))

    def matvec(self, x: List[float]) -> List[float]:
        m, n = self.shape
        y = [0.0] * m
        for k, off in enumerate(self.offsets):
            for i in range(m):
                j = i + off
                if 0 <= j < n:
                    y[i] += self.data[k][i] * x[j]
        return y

if __name__ == "__main__":
    dense = [[2.0, 1.0, 0.0], [0.0, 3.0, 1.0], [0.0, 0.0, 4.0]]
    dia = DIAMatrix.from_dense(dense)
    y = dia.matvec([1.0, 1.0, 1.0])
    assert abs(y[0] - 3.0) < 1e-9 and abs(y[2] - 4.0) < 1e-9
    print("dia self-test passed", y)
