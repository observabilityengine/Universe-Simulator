"""
Universe Simulator - DOK (Dictionary of Keys) Sparse Matrix
Original dict-based sparse format with conversion.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

class DOKMatrix:
    def __init__(self, shape: Tuple[int, int]):
        self.shape = shape
        self.data: Dict[Tuple[int, int], float] = {}

    def __setitem__(self, key: Tuple[int, int], value: float) -> None:
        if abs(value) > 1e-15:
            self.data[key] = value
        elif key in self.data:
            del self.data[key]

    def __getitem__(self, key: Tuple[int, int]) -> float:
        return self.data.get(key, 0.0)

    def to_dense(self) -> List[List[float]]:
        m, n = self.shape
        dense = [[0.0] * n for _ in range(m)]
        for (i, j), v in self.data.items():
            dense[i][j] = v
        return dense

    def matvec(self, x: List[float]) -> List[float]:
        y = [0.0] * self.shape[0]
        for (i, j), v in self.data.items():
            y[i] += v * x[j]
        return y

if __name__ == "__main__":
    dok = DOKMatrix((3, 3))
    dok[0, 0] = 1.0
    dok[0, 2] = 2.0
    dok[2, 2] = 5.0
    y = dok.matvec([1.0, 0.0, 1.0])
    assert abs(y[0] - 3.0) < 1e-9 and abs(y[2] - 5.0) < 1e-9
    print("dok self-test passed", y)
