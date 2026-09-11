"""Frequency-domain bandpass / lowpass / highpass filter via FFT."""
from __future__ import annotations
import math
from typing import List
from .fft import fft, ifft


def fft_filter(
    x: List[float],
    sample_rate: float,
    low_hz: float = 0.0,
    high_hz: float = None,
) -> List[float]:
    X = fft(x)
    n = len(X)
    if high_hz is None:
        high_hz = sample_rate / 2
    out_spec = []
    for k, val in enumerate(X):
        # frequency for bin k
        freq = k * sample_rate / n if k <= n // 2 else (k - n) * sample_rate / n
        freq = abs(freq)
        if low_hz <= freq <= high_hz:
            out_spec.append(val)
        else:
            out_spec.append(0j)
    y = ifft(out_spec)
    return y[: len(x)]


if __name__ == "__main__":
    sr = 100.0
    x = [math.sin(2 * math.pi * 5 * i / sr) + math.sin(2 * math.pi * 30 * i / sr) for i in range(128)]
    y = fft_filter(x, sr, low_hz=0, high_hz=10)
    assert len(y) == len(x)
    print("fft_filter self-tests passed")
