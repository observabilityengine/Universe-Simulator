"""Triangle rasterization with barycentric coordinates."""
from __future__ import annotations
from typing import List, Tuple
from .barycentric import barycentric
from .rasterizer import Framebuffer, put_pixel

Vec2 = Tuple[float, float]
Color = Tuple[float, float, float]


def fill_triangle(fb: Framebuffer, v0: Vec2, v1: Vec2, v2: Vec2, color: Color) -> None:
    min_x = int(min(v0[0], v1[0], v2[0]))
    max_x = int(max(v0[0], v1[0], v2[0]))
    min_y = int(min(v0[1], v1[1], v2[1]))
    max_y = int(max(v0[1], v1[1], v2[1]))
    h, w = len(fb), len(fb[0])
    for y in range(max(0, min_y), min(h, max_y + 1)):
        for x in range(max(0, min_x), min(w, max_x + 1)):
            w0, w1, w2 = barycentric(v0, v1, v2, (x + 0.5, y + 0.5))
            if w0 >= 0 and w1 >= 0 and w2 >= 0:
                put_pixel(fb, x, y, color)


if __name__ == "__main__":
    from .rasterizer import create_framebuffer
    fb = create_framebuffer(20, 20)
    fill_triangle(fb, (2, 2), (18, 5), (10, 18), (0.0, 1.0, 0.0))
    filled = sum(1 for row in fb for p in row if p[1] > 0.5)
    assert filled > 10
    print(f"triangle_raster filled={filled}")
    print("triangle_raster self-tests passed")
