"""Simple grid-based spatial index."""
from __future__ import annotations
from typing import Dict, List, Tuple

Point = Tuple[float, float]


class GridIndex:
    def __init__(self, cell_size: float = 1.0):
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], List[Point]] = {}

    def _key(self, p: Point) -> Tuple[int, int]:
        return int(p[0] // self.cell_size), int(p[1] // self.cell_size)

    def insert(self, p: Point) -> None:
        k = self._key(p)
        self.grid.setdefault(k, []).append(p)

    def query(self, bbox: Tuple[float, float, float, float]) -> List[Point]:
        x0, y0, x1, y1 = bbox
        result = []
        for i in range(int(x0 // self.cell_size), int(x1 // self.cell_size) + 1):
            for j in range(int(y0 // self.cell_size), int(y1 // self.cell_size) + 1):
                for p in self.grid.get((i, j), []):
                    if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                        result.append(p)
        return result


if __name__ == "__main__":
    g = GridIndex(1.0)
    g.insert((0.5, 0.5))
    g.insert((2.5, 2.5))
    res = g.query((0, 0, 1, 1))
    assert (0.5, 0.5) in res
    print(f"spatial_index {res}")
    print("spatial_index self-tests passed")
