"""
Universe Simulator - CSR Sparse Matrix + matvec
Original compressed sparse row format.
"""

from __future__ import annotations

from typing import List, Tuple

class CSRMatrix:
    def __init__(self, data: List[float], indices: List[int], indptr: List[int], shape: Tuple[int, int]):
        self.data = data
        self.indices = indices
        self.indptr = indptr
        self.shape = shape

    @classmethod
    def from_dense(cls, dense: List[List[float]]) -> "CSRMatrix":
        data, indices, indptr = [], [], [0]
        for row in dense:
            for j, v in enumerate(row):
                if abs(v) > 1e-15:
                    data.append(v)
                    indices.append(j)
            indptr.append(len(data))
        return cls(data, indices, indptr, (len(dense), len(dense[0]) if dense else 0))

    def matvec(self, x: List[float]) -> List[float]:
        m, n = self.shape
        y = [0.0] * m
        for i in range(m):
            for k in range(self.indptr[i], self.indptr[i + 1]):
                y[i] += self.data[k] * x[self.indices[k]]
        return y

if __name__ == "__main__":
    dense = [[1.0, 0.0, 2.0], [0.0, 3.0, 0.0], [4.0, 0.0, 5.0]]
    csr = CSRMatrix.from_dense(dense)
    y = csr.matvec([1.0, 1.0, 1.0])
    assert abs(y[0] - 3.0) < 1e-9 and abs(y[1] - 3.0) < 1e-9
    print("sparse_csr self-test passed", y)
