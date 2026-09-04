"""
Universe Simulator - LIL (List of Lists) Sparse Matrix
Original row-based sparse format.
"""

from __future__ import annotations

from typing import List, Tuple

class LILMatrix:
    def __init__(self, shape: Tuple[int, int]):
        self.shape = shape
        self.rows: List[List[Tuple[int, float]]] = [[] for _ in range(shape[0])]

    def __setitem__(self, key: Tuple[int, int], value: float) -> None:
        i, j = key
        row = self.rows[i]
        for k, (col, _) in enumerate(row):
            if col == j:
                if abs(value) > 1e-15:
                    row[k] = (j, value)
                else:
                    del row[k]
                return
            if col > j:
                if abs(value) > 1e-15:
                    row.insert(k, (j, value))
                return
        if abs(value) > 1e-15:
            row.append((j, value))

    def matvec(self, x: List[float]) -> List[float]:
        y = [0.0] * self.shape[0]
        for i, row in enumerate(self.rows):
            for j, v in row:
                y[i] += v * x[j]
        return y

if __name__ == "__main__":
    lil = LILMatrix((3, 3))
    lil[0, 0] = 1.0
    lil[0, 2] = 2.0
    lil[1, 1] = 3.0
    y = lil.matvec([1.0, 1.0, 1.0])
    assert abs(y[0] - 3.0) < 1e-9 and abs(y[1] - 3.0) < 1e-9
    print("lil self-test passed", y)
