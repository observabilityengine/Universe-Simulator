"""
Universe Simulator - ELLPACK Sparse Matrix
Original fixed-width row storage + matvec.
"""

from __future__ import annotations

from typing import List, Tuple

class ELLMatrix:
    def __init__(self, data: List[List[float]], indices: List[List[int]], shape: Tuple[int, int]):
        self.data = data
        self.indices = indices
        self.shape = shape

    @classmethod
    def from_dense(cls, dense: List[List[float]], max_nnz: int = 4) -> "ELLMatrix":
        m = len(dense)
        n = len(dense[0]) if dense else 0
        data = [[0.0]*max_nnz for _ in range(m)]
        indices = [[-1]*max_nnz for _ in range(m)]
        for i in range(m):
            k = 0
            for j in range(n):
                if abs(dense[i][j]) > 1e-15 and k < max_nnz:
                    data[i][k] = dense[i][j]
                    indices[i][k] = j
                    k += 1
        return cls(data, indices, (m, n))

    def matvec(self, x: List[float]) -> List[float]:
        m, _ = self.shape
        y = [0.0] * m
        for i in range(m):
            for k, j in enumerate(self.indices[i]):
                if j >= 0:
                    y[i] += self.data[i][k] * x[j]
        return y

if __name__ == "__main__":
    dense = [[1.0, 0.0, 2.0], [0.0, 3.0, 0.0], [4.0, 0.0, 5.0]]
    ell = ELLMatrix.from_dense(dense)
    y = ell.matvec([1.0, 1.0, 1.0])
    assert abs(y[0] - 3.0) < 1e-9
    print("ellpack self-test passed", y)
