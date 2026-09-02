"""
Module 30 – Fractal Generator
Mandelbrot and Julia set escape-time algorithms.
Original, executable implementation.
"""

from __future__ import annotations
import numpy as np
from typing import Tuple


def mandelbrot(
    width: int = 200,
    height: int = 150,
    x_range: Tuple[float, float] = (-2.0, 0.5),
    y_range: Tuple[float, float] = (-1.25, 1.25),
    max_iter: int = 80,
) -> np.ndarray:
    xs = np.linspace(x_range[0], x_range[1], width)
    ys = np.linspace(y_range[0], y_range[1], height)
    result = np.zeros((height, width), dtype=np.int32)

    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            c = complex(x, y)
            z = 0j
            it = 0
            while abs(z) <= 2.0 and it < max_iter:
                z = z * z + c
                it += 1
            result[i, j] = it
    return result


def julia(
    c: complex = -0.4 + 0.6j,
    width: int = 200,
    height: int = 150,
    x_range: Tuple[float, float] = (-1.5, 1.5),
    y_range: Tuple[float, float] = (-1.5, 1.5),
    max_iter: int = 80,
) -> np.ndarray:
    xs = np.linspace(x_range[0], x_range[1], width)
    ys = np.linspace(y_range[0], y_range[1], height)
    result = np.zeros((height, width), dtype=np.int32)

    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            z = complex(x, y)
            it = 0
            while abs(z) <= 2.0 and it < max_iter:
                z = z * z + c
                it += 1
            result[i, j] = it
    return result


if __name__ == "__main__":
    print("Testing Fractal Generator...")
    m = mandelbrot(width=80, height=40, max_iter=50)
    print(f"  Mandelbrot shape: {m.shape}  max iter reached: {m.max()}")
    center = m[15:25, 30:50]
    for row in center:
        print("  " + "".join(" .:-=+*#%@"[min(v * 9 // 50, 9)] for v in row))
    j = julia(width=60, height=30)
    print(f"  Julia shape: {j.shape}")
    print("Fractal Generator module OK.")
