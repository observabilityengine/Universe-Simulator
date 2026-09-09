"""Cosmic web classification – voids, sheets, filaments, knots via tidal tensor."""
from __future__ import annotations
import math
from typing import List


def tidal_eigenvalues(density_hess: List[List[float]]) -> List[float]:
    a, b, c = density_hess[0][0], density_hess[1][1], density_hess[2][2]
    d, e, f = density_hess[0][1], density_hess[0][2], density_hess[1][2]
    q = (a + b + c) / 3
    p2 = (a - q) ** 2 + (b - q) ** 2 + (c - q) ** 2 + 2 * (d * d + e * e + f * f)
    p = math.sqrt(p2 / 6) if p2 > 0 else 1e-12
    B00, B11, B22 = (a - q) / p, (b - q) / p, (c - q) / p
    B01, B02, B12 = d / p, e / p, f / p
    det_b = B00 * (B11 * B22 - B12 * B12) - B01 * (B01 * B22 - B12 * B02) + B02 * (B01 * B12 - B11 * B02)
    r = max(-1, min(1, det_b / 2))
    phi = math.acos(r) / 3
    eig = [q + 2 * p * math.cos(phi), q + 2 * p * math.cos(phi + 2 * math.pi / 3), q + 2 * p * math.cos(phi + 4 * math.pi / 3)]
    return sorted(eig, reverse=True)


def classify_web(eigenvalues: List[float], threshold: float = 0.0) -> str:
    n = sum(1 for e in eigenvalues if e > threshold)
    return ["void", "sheet", "filament", "knot"][n]


if __name__ == "__main__":
    H = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
    ev = tidal_eigenvalues(H)
    assert classify_web(ev) == "knot"
    H0 = [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    assert classify_web(tidal_eigenvalues(H0)) == "void"
    print(f"cosmic_web ev={ev}")
    print("cosmic_web self-tests passed")
