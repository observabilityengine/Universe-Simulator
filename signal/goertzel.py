"""
Universe Simulator - Goertzel Algorithm (single-bin DFT)
Original implementation for detecting a target frequency.
"""

from __future__ import annotations

import math
from typing import List


def goertzel(samples: List[float], target_freq: float, sample_rate: float) -> complex:
    n = len(samples)
    k = int(0.5 + (n * target_freq) / sample_rate)
    w = 2 * math.pi * k / n
    coeff = 2 * math.cos(w)
    s0 = s1 = s2 = 0.0
    for x in samples:
        s0 = x + coeff * s1 - s2
        s2 = s1
        s1 = s0
    real = s1 - s2 * math.cos(w)
    imag = s2 * math.sin(w)
    return complex(real, imag)


if __name__ == "__main__":
    sr = 8000.0
    f = 440.0
    samples = [math.sin(2 * math.pi * f * i / sr) for i in range(256)]
    c = goertzel(samples, f, sr)
    mag = abs(c)
    assert mag > 50  # strong response at target
    c2 = goertzel(samples, 1000.0, sr)
    assert abs(c2) < mag * 0.3
    print("goertzel self-test passed", mag)
