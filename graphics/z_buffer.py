"""Z-buffer depth testing."""
from __future__ import annotations
from typing import List, Tuple

Color = Tuple[float, float, float]


class ZBuffer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.color = [[(0.0, 0.0, 0.0) for _ in range(width)] for _ in range(height)]
        self.depth = [[float("inf") for _ in range(width)] for _ in range(height)]

    def test_and_set(self, x: int, y: int, z: float, color: Color) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if z < self.depth[y][x]:
            self.depth[y][x] = z
            self.color[y][x] = color
            return True
        return False

    def clear(self, color: Color = (0.0, 0.0, 0.0)) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.color[y][x] = color
                self.depth[y][x] = float("inf")


if __name__ == "__main__":
    zb = ZBuffer(10, 10)
    assert zb.test_and_set(5, 5, 1.0, (1, 0, 0))
    assert not zb.test_and_set(5, 5, 2.0, (0, 1, 0))
    assert zb.test_and_set(5, 5, 0.5, (0, 0, 1))
    assert zb.color[5][5] == (0, 0, 1)
    print("z_buffer self-tests passed")
