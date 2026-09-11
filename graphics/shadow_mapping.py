"""Shadow map depth comparison."""
from __future__ import annotations
from typing import List


class ShadowMap:
    def __init__(self, size: int = 64):
        self.size = size
        self.depth = [[1.0 for _ in range(size)] for _ in range(size)]

    def write(self, x: int, y: int, z: float) -> None:
        if 0 <= x < self.size and 0 <= y < self.size:
            if z < self.depth[y][x]:
                self.depth[y][x] = z

    def in_shadow(self, x: int, y: int, z: float, bias: float = 0.005) -> bool:
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        return z > self.depth[y][x] + bias


if __name__ == "__main__":
    sm = ShadowMap(16)
    sm.write(8, 8, 0.5)
    assert sm.in_shadow(8, 8, 0.7)
    assert not sm.in_shadow(8, 8, 0.4)
    print("shadow_mapping self-tests passed")
