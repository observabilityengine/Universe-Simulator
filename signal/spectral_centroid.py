"""
Universe Simulator - Spectral Centroid
Original magnitude-spectrum weighted average frequency.
"""

from __future__ import annotations

import math
from typing import List

def spectral_centroid(samples: List[float], sample_rate: float) -> float:
    n = len(samples)
    # simple DFT magnitude
    mags = []
    freqs = []
    for k in range(n // 2):
        re = sum(samples[i] * math.cos(2 * math.pi * k * i / n) for i in range(n))
        im = sum(samples[i] * math.sin(2 * math.pi * k * i / n) for i in range(n))
        mags.append(math.sqrt(re*re + im*im))
        freqs.append(k * sample_rate / n)
    total = sum(mags) + 1e-12
    return sum(f * m for f, m in zip(freqs, mags)) / total

if __name__ == "__main__":
    sr = 8000.0
    f0 = 440.0
    samples = [math.sin(2 * math.pi * f0 * i / sr) for i in range(256)]
    sc = spectral_centroid(samples, sr)
    assert abs(sc - f0) < 50
    print("spectral_centroid self-test passed", sc)
