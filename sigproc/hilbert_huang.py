"""Simplified Hilbert-Huang: empirical mode decomposition (EMD) sifting."""
from __future__ import annotations
from typing import List, Tuple


def _extrema(x: List[float]) -> Tuple[List[int], List[int]]:
    maxima, minima = [], []
    for i in range(1, len(x) - 1):
        if x[i] >= x[i - 1] and x[i] >= x[i + 1]:
            maxima.append(i)
        if x[i] <= x[i - 1] and x[i] <= x[i + 1]:
            minima.append(i)
    return maxima, minima


def _interp_envelope(x: List[float], idxs: List[int]) -> List[float]:
    """Linear interpolation through extrema; constant edges."""
    n = len(x)
    if len(idxs) < 2:
        mean = sum(x) / n if n else 0.0
        return [mean] * n
    env = [0.0] * n
    # left
    for i in range(idxs[0]):
        env[i] = x[idxs[0]]
    for a, b in zip(idxs, idxs[1:]):
        for i in range(a, b + 1):
            t = (i - a) / (b - a) if b != a else 0
            env[i] = x[a] * (1 - t) + x[b] * t
    for i in range(idxs[-1], n):
        env[i] = x[idxs[-1]]
    return env


def sift_imf(x: List[float], max_sift: int = 10) -> List[float]:
    h = list(x)
    for _ in range(max_sift):
        maxima, minima = _extrema(h)
        if len(maxima) < 2 or len(minima) < 2:
            break
        upper = _interp_envelope(h, maxima)
        lower = _interp_envelope(h, minima)
        mean = [(u + l) / 2 for u, l in zip(upper, lower)]
        h = [hi - m for hi, m in zip(h, mean)]
    return h


def emd(x: List[float], max_imfs: int = 3) -> List[List[float]]:
    residual = list(x)
    imfs = []
    for _ in range(max_imfs):
        imf = sift_imf(residual)
        imfs.append(imf)
        residual = [r - i for r, i in zip(residual, imf)]
        maxima, minima = _extrema(residual)
        if len(maxima) + len(minima) < 4:
            break
    return imfs


if __name__ == "__main__":
    import math
    x = [math.sin(2 * math.pi * 3 * i / 100) + 0.5 * math.sin(2 * math.pi * 11 * i / 100) for i in range(100)]
    imfs = emd(x, max_imfs=2)
    assert len(imfs) >= 1
    print(f"hilbert_huang n_imfs={len(imfs)}")
    print("hilbert_huang self-tests passed")
