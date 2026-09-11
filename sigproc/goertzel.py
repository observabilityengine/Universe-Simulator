"""Goertzel algorithm for single-frequency DFT bin."""
from __future__ import annotations
import math
from typing import List


def goertzel(samples: List[float], freq: float, sample_rate: float) -> complex:
    n = len(samples)
    k = int(0.5 + (n * freq) / sample_rate)
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


def goertzel_power(samples: List[float], freq: float, sample_rate: float) -> float:
    c = goertzel(samples, freq, sample_rate)
    return abs(c) ** 2


if __name__ == "__main__":
    sr = 100.0
    n = 100
    freq = 10.0
    samples = [math.sin(2 * math.pi * freq * i / sr) for i in range(n)]
    p_target = goertzel_power(samples, 10.0, sr)
    p_other = goertzel_power(samples, 25.0, sr)
    assert p_target > p_other
    print(f"goertzel power_10={p_target:.1f} power_25={p_other:.1f}")
    print("goertzel self-tests passed")
