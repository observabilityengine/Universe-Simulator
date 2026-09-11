"""IIR notch filter (2nd order)."""
from __future__ import annotations
import math
from typing import List
from .biquad import Biquad


def notch_coeffs(f0: float, fs: float, q: float = 10.0):
    w0 = 2 * math.pi * f0 / fs
    alpha = math.sin(w0) / (2 * q)
    cosw = math.cos(w0)
    b0 = 1.0
    b1 = -2 * cosw
    b2 = 1.0
    a0 = 1 + alpha
    a1 = -2 * cosw
    a2 = 1 - alpha
    return b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0


def notch_filter(data: List[float], f0: float, fs: float, q: float = 10.0) -> List[float]:
    b0, b1, b2, a1, a2 = notch_coeffs(f0, fs, q)
    return Biquad(b0, b1, b2, a1, a2).process_block(data)


if __name__ == "__main__":
    import math as m
    fs = 100.0
    x = [m.sin(2 * m.pi * 10 * i / fs) + m.sin(2 * m.pi * 25 * i / fs) for i in range(200)]
    y = notch_filter(x, 10.0, fs, q=5.0)
    assert len(y) == len(x)
    print("iir_notch self-tests passed")
