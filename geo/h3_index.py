"""Simplified H3-like hierarchical hexagonal index (grid approximation)."""
from __future__ import annotations
import math
from typing import Tuple


def h3_approx(lat: float, lon: float, resolution: int = 5) -> str:
    scale = 2 ** resolution
    i = int((lat + 90) / 180 * scale)
    j = int((lon + 180) / 360 * scale)
    return f"h3r{resolution}_{i}_{j}"


def h3_neighbors(index: str) -> list:
    parts = index.split("_")
    res, i, j = int(parts[0][3:]), int(parts[1]), int(parts[2])
    return [f"h3r{res}_{i+di}_{j+dj}" for di in (-1, 0, 1) for dj in (-1, 0, 1) if not (di == 0 and dj == 0)]


if __name__ == "__main__":
    idx = h3_approx(37.7, -122.4, 4)
    nbs = h3_neighbors(idx)
    assert len(nbs) == 8
    print(f"h3_index {idx} neighbors={len(nbs)}")
    print("h3_index self-tests passed")
