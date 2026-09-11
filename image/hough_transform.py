"""Hough line transform."""
from __future__ import annotations
import math
from typing import List, Tuple

Image = List[List[float]]


def hough_lines(edges: Image, threshold: int = 5) -> List[Tuple[float, float]]:
    h, w = len(edges), len(edges[0])
    max_rho = int(math.sqrt(h * h + w * w))
    n_theta = 180
    acc = [[0] * n_theta for _ in range(2 * max_rho + 1)]
    for y in range(h):
        for x in range(w):
            if edges[y][x] < 0.5:
                continue
            for t in range(n_theta):
                theta = math.radians(t)
                rho = int(x * math.cos(theta) + y * math.sin(theta)) + max_rho
                if 0 <= rho < len(acc):
                    acc[rho][t] += 1
    lines = []
    for rho_i in range(len(acc)):
        for t in range(n_theta):
            if acc[rho_i][t] >= threshold:
                lines.append((rho_i - max_rho, math.radians(t)))
    return lines


if __name__ == "__main__":
    edges = [[0]*10 for _ in range(10)]
    for i in range(10):
        edges[i][5] = 1.0
    lines = hough_lines(edges, threshold=3)
    assert len(lines) > 0
    print(f"hough_transform n_lines={len(lines)}")
    print("hough_transform self-tests passed")
