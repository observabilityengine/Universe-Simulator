"""Texture sampling with bilinear interpolation."""
from __future__ import annotations
from typing import List, Tuple

Color = Tuple[float, float, float]
Texture = List[List[Color]]


def sample(tex: Texture, u: float, v: float) -> Color:
    h, w = len(tex), len(tex[0])
    u = u % 1.0
    v = v % 1.0
    x = u * (w - 1)
    y = v * (h - 1)
    x0, y0 = int(x), int(y)
    x1, y1 = min(x0 + 1, w - 1), min(y0 + 1, h - 1)
    fx, fy = x - x0, y - y0
    def lerp(a, b, t):
        return (a[0]*(1-t)+b[0]*t, a[1]*(1-t)+b[1]*t, a[2]*(1-t)+b[2]*t)
    c00, c10 = tex[y0][x0], tex[y0][x1]
    c01, c11 = tex[y1][x0], tex[y1][x1]
    return lerp(lerp(c00, c10, fx), lerp(c01, c11, fx), fy)


if __name__ == "__main__":
    tex = [[(1,0,0), (0,1,0)], [(0,0,1), (1,1,1)]]
    c = sample(tex, 0.25, 0.25)
    assert c[0] > 0.5
    print(f"texture_mapping {c}")
    print("texture_mapping self-tests passed")
