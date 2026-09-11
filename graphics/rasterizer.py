"""Software rasterizer – clear, put pixel, draw line."""
from __future__ import annotations
from typing import List, Tuple

Color = Tuple[float, float, float]
Framebuffer = List[List[Color]]


def create_framebuffer(width: int, height: int, clear: Color = (0.0, 0.0, 0.0)) -> Framebuffer:
    return [[clear for _ in range(width)] for _ in range(height)]


def put_pixel(fb: Framebuffer, x: int, y: int, color: Color) -> None:
    h, w = len(fb), len(fb[0])
    if 0 <= x < w and 0 <= y < h:
        fb[y][x] = color


def draw_line(fb: Framebuffer, x0: int, y0: int, x1: int, y1: int, color: Color) -> None:
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        put_pixel(fb, x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


if __name__ == "__main__":
    fb = create_framebuffer(10, 10)
    draw_line(fb, 0, 0, 9, 9, (1.0, 0.0, 0.0))
    assert fb[5][5][0] == 1.0
    print("rasterizer self-tests passed")
