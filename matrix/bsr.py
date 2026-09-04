"""
Universe Simulator - BSR (Block Sparse Row) Matrix
Original block-compressed sparse row + matvec.
"""

from __future__ import annotations

from typing import List, Tuple

class BSRMatrix:
    def __init__(self, data: List[List[List[float]]], indices: List[int], indptr: List[int], shape: Tuple[int, int], block_size: int):
        self.data = data
        self.indices = indices
        self.indptr = indptr
        self.shape = shape
        self.blocksize = block_size

    @classmethod
    def from_dense(cls, dense: List[List[float]], block_size: int = 2) -> "BSRMatrix":
        m = len(dense)
        n = len(dense[0]) if dense else 0
        bm, bn = (m + block_size - 1) // block_size, (n + block_size - 1) // block_size
        data, indices, indptr = [], [], [0]
        for bi in range(bm):
            for bj in range(bn):
                block = [[0.0]*block_size for _ in range(block_size)]
                nonzero = False
                for i in range(block_size):
                    for j in range(block_size):
                        ii, jj = bi*block_size + i, bj*block_size + j
                        if ii < m and jj < n and abs(dense[ii][jj]) > 1e-15:
                            block[i][j] = dense[ii][jj]
                            nonzero = True
                if nonzero:
                    data.append(block)
                    indices.append(bj)
            indptr.append(len(data))
        return cls(data, indices, indptr, (m, n), block_size)

    def matvec(self, x: List[float]) -> List[float]:
        m, n = self.shape
        y = [0.0] * m
        bs = self.blocksize
        for bi in range(len(self.indptr) - 1):
            for k in range(self.indptr[bi], self.indptr[bi+1]):
                bj = self.indices[k]
                block = self.data[k]
                for i in range(bs):
                    for j in range(bs):
                        ii, jj = bi*bs + i, bj*bs + j
                        if ii < m and jj < n:
                            y[ii] += block[i][j] * x[jj]
        return y

if __name__ == "__main__":
    dense = [[1.0, 2.0, 0.0, 0.0], [3.0, 4.0, 0.0, 0.0], [0.0, 0.0, 5.0, 6.0], [0.0, 0.0, 7.0, 8.0]]
    bsr = BSRMatrix.from_dense(dense, 2)
    y = bsr.matvec([1.0, 1.0, 1.0, 1.0])
    assert abs(y[0] - 3.0) < 1e-9 and abs(y[2] - 11.0) < 1e-9
    print("bsr self-test passed", y)
