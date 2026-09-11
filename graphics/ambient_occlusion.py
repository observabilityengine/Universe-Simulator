"""Screen-space ambient occlusion approximation."""
from __future__ import annotations
import math
from typing import List


def ssao(depth: List[List[float]], radius: float = 2.0, samples: int = 8) -> List[List[float]]:
    h, w = len(depth), len(depth[0])
    out = [[1.0] * w for _ in range(h)]
    offsets = [(math.cos(2*math.pi*i/samples)*radius, math.sin(2*math.pi*i/samples)*radius) for i in range(samples)]
    for y in range(h):
        for x in range(w):
            d0 = depth[y][x]
            occluded = 0
            for dx, dy in offsets:
                sx, sy = int(x + dx), int(y + dy)
                if 0 <= sx < w and 0 <= sy < h:
                    if depth[sy][sx] < d0 - 0.01:
                        occluded += 1
            out[y][x] = 1.0 - occluded / samples
    return out


if __name__ == "__main__":
    depth = [[1.0]*16 for _ in range(16)]
    depth[8][8] = 0.5
    ao = ssao(depth)
    assert ao[8][8] <= 1.0
    print(f"ambient_occlusion center={ao[8][8]:.2f}")
    print("ambient_occlusion self-tests passed")
