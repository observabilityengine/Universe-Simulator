"""Wiener filter for noise reduction (spectral subtraction form)."""
from __future__ import annotations
import math
from typing import List
from .fft import fft, ifft


def wiener_filter(noisy: List[float], noise_power: float = 0.1) -> List[float]:
    X = fft(noisy)
    filtered = []
    for z in X:
        p = abs(z) ** 2
        gain = max(p - noise_power, 0.0) / (p + 1e-12)
        filtered.append(z * gain)
    y = ifft(filtered)
    return y[: len(noisy)]


if __name__ == "__main__":
    import random
    rng = random.Random(0)
    clean = [math.sin(2 * math.pi * 3 * i / 64) for i in range(64)]
    noisy = [c + 0.2 * rng.gauss(0, 1) for c in clean]
    out = wiener_filter(noisy, noise_power=0.05)
    assert len(out) == 64
    print("wiener self-tests passed")
