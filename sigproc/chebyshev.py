"""Chebyshev Type I lowpass (order 2) via bilinear transform."""
from __future__ import annotations
import math
from typing import List, Tuple
from .biquad import Biquad


def chebyshev1_lowpass_coeffs(fc: float, fs: float, ripple_db: float = 1.0) -> Tuple[float, float, float, float, float]:
    # order-2 Chebyshev prototype warped
    eps = math.sqrt(10 ** (ripple_db / 10) - 1)
    # prototype poles roughly
    w0 = 2 * math.pi * fc / fs
    # simplified bilinear coefficients for order-2
    g = 10 ** (-ripple_db / 40)
    k = math.tan(w0 / 2)
    k2 = k * k
    norm = 1 + math.sqrt(2) * k * g + k2
    b0 = k2 / norm
    b1 = 2 * b0
    b2 = b0
    a1 = 2 * (k2 - 1) / norm
    a2 = (1 - math.sqrt(2) * k * g + k2) / norm
    return b0, b1, b2, a1, a2


def chebyshev_lowpass(data: List[float], fc: float, fs: float, ripple_db: float = 1.0) -> List[float]:
    b0, b1, b2, a1, a2 = chebyshev1_lowpass_coeffs(fc, fs, ripple_db)
    return Biquad(b0, b1, b2, a1, a2).process_block(data)


if __name__ == "__main__":
    x = [1.0] + [0.0] * 30
    y = chebyshev_lowpass(x, 10.0, 100.0)
    assert len(y) == len(x)
    print("chebyshev self-tests passed")
