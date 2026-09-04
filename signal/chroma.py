"""
Universe Simulator - Chroma Feature Extraction
Original 12-bin pitch class profile from spectrum.
"""

from __future__ import annotations

import math
from typing import List

def chroma(samples: List[float], sample_rate: float = 22050.0) -> List[float]:
    n = len(samples)
    # magnitude spectrum
    mags = []
    for k in range(1, n // 2):
        re = sum(samples[i] * math.cos(2 * math.pi * k * i / n) for i in range(n))
        im = sum(samples[i] * math.sin(2 * math.pi * k * i / n) for i in range(n))
        mags.append(math.sqrt(re*re + im*im))
    # map to 12 chroma bins
    chroma_bins = [0.0] * 12
    for k, mag in enumerate(mags, 1):
        freq = k * sample_rate / n
        if freq < 20:
            continue
        midi = 69 + 12 * math.log2(freq / 440.0)
        bin_idx = int(round(midi)) % 12
        chroma_bins[bin_idx] += mag
    total = sum(chroma_bins) + 1e-12
    return [c / total for c in chroma_bins]

if __name__ == "__main__":
    samples = [math.sin(2 * math.pi * 440 * i / 22050) for i in range(2048)]
    ch = chroma(samples)
    assert abs(sum(ch) - 1.0) < 1e-6
    assert ch[9] > 0.1  # A is midi 69 -> bin 9
    print("chroma self-test passed", ch[9])
