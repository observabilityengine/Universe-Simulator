"""Supersample antialiasing."""
from __future__ import annotations
from typing import Callable, List, Tuple

Color = Tuple[float, float, float]


def supersample(
    shade_fn: Callable[[float, float], Color],
    width: int,
    height: int,
    samples: int = 2,
) -> List[List[Color]]:
    img = []
    for j in range(height):
        row = []
        for i in range(width):
            r = g = b = 0.0
            for sy in range(samples):
                for sx in range(samples):
                    u = (i + (sx + 0.5) / samples) / width
                    v = (j + (sy + 0.5) / samples) / height
                    c = shade_fn(u, v)
                    r += c[0]; g += c[1]; b += c[2]
            n = samples * samples
            row.append((r/n, g/n, b/n))
        img.append(row)
    return img


if __name__ == "__main__":
    def checker(u, v):
        return (1.0, 1.0, 1.0) if int(u*8) % 2 == int(v*8) % 2 else (0.0, 0.0, 0.0)
    img = supersample(checker, 16, 16, 2)
    assert len(img) == 16
    print("antialiasing self-tests passed")
