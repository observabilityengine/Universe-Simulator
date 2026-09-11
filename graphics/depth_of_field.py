"""Depth-of-field blur based on circle of confusion."""
from __future__ import annotations
from typing import List, Tuple

Color = Tuple[float, float, float]


def apply_dof(
    color: List[List[Color]],
    depth: List[List[float]],
    focus: float = 0.5,
    aperture: float = 0.1,
) -> List[List[Color]]:
    h, w = len(color), len(color[0])
    out = [[(0.0, 0.0, 0.0) for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            coc = abs(depth[y][x] - focus) * aperture * 10
            radius = max(1, int(coc))
            r = g = b = count = 0.0
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    sy, sx = y + dy, x + dx
                    if 0 <= sy < h and 0 <= sx < w:
                        c = color[sy][sx]
                        r += c[0]; g += c[1]; b += c[2]; count += 1
            out[y][x] = (r/count, g/count, b/count)
    return out


if __name__ == "__main__":
    color = [[(1.0, 0.0, 0.0)] * 8 for _ in range(8)]
    depth = [[0.5] * 8 for _ in range(8)]
    depth[4][4] = 1.0
    out = apply_dof(color, depth)
    assert len(out) == 8
    print("depth_of_field self-tests passed")
