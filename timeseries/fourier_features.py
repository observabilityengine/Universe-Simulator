"""Fourier seasonal features."""
from __future__ import annotations
import math
from typing import List, Tuple


def fourier_features(t: List[float], period: float = 12.0, order: int = 3) -> List[List[float]]:
    features = []
    for ti in t:
        row = []
        for k in range(1, order + 1):
            row.append(math.sin(2 * math.pi * k * ti / period))
            row.append(math.cos(2 * math.pi * k * ti / period))
        features.append(row)
    return features


if __name__ == "__main__":
    feats = fourier_features(list(range(12)), 12, 2)
    assert len(feats) == 12 and len(feats[0]) == 4
    print("fourier_features self-tests passed")
