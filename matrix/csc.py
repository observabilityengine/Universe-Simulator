"""
Universe Simulator - CSC Sparse Matrix
Original compressed sparse column + matvec.
"""

from __future__ import annotations

from typing import List, Tuple

class CSCMatrix:
    def __init__(self, data: List[float], indices: List[int], indptr: List[int], shape: Tuple[int, int]):
        self.data = data
        self.indices = indices
        self.indptr = indptr
        self.shape = shape

    @classmethod
    def from_dense(cls, dense: List[List[float]]) -> "CSCMatrix":
        m = len(dense)
        n = len(dense[0]) if dense else 0
        data, indices, indptr = [], [], [0]
        for j in range(n):
            for i in range(m):
                if abs(dense[i][j]) > 1e-15:
                    data.append(dense[i][j])
                    indices.append(i)
            indptr.append(len(data))
        return cls(data, indices, indptr, (m, n))

    def matvec(self, x: List[float]) -> List[float]:
        m, n = self.shape
        y = [0.0] * m
        for j in range(n):
            for k in range(self.indptr[j], self.indptr[j+1]):
                y[self.indices[k]] += self.data[k] * x[j]
        return y

if __name__ == "__main__":
    dense = [[1.0, 0.0, 2.0], [0.0, 3.0, 0.0], [4.0, 0.0, 5.0]]
    csc = CSCMatrix.from_dense(dense)
    y = csc.matvec([1.0, 1.0, 1.0])
    assert abs(y[0] - 3.0) < 1e-9 and abs(y[2] - 9.0) < 1e-9
    print("csc self-test passed", y)
