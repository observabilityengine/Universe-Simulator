"""Spectral centroid of a magnitude spectrum."""
from __future__ import annotations
from typing import List
from .fft import fft


def spectral_centroid(x: List[float], sample_rate: float) -> float:
    X = fft(x)
    n = len(X)
    mags = [abs(X[k]) for k in range(n // 2 + 1)]
    freqs = [k * sample_rate / n for k in range(len(mags))]
    num = sum(f * m for f, m in zip(freqs, mags))
    den = sum(mags) or 1e-12
    return num / den


if __name__ == "__main__":
    import math
    sr = 100.0
    x = [math.sin(2 * math.pi * 10 * i / sr) for i in range(100)]
    c = spectral_centroid(x, sr)
    assert 5 < c < 20
    print(f"spectral_centroid {c:.2f} Hz")
    print("spectral_centroid self-tests passed")
