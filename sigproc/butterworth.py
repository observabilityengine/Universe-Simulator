"""Butterworth lowpass via cascaded biquads (order 2)."""
from __future__ import annotations
import math
from typing import List
from .biquad import Biquad, lowpass_coeffs


def butterworth_lowpass(data: List[float], fc: float, fs: float) -> List[float]:
    b0, b1, b2, a1, a2 = lowpass_coeffs(fc, fs, q=0.7071)
    filt = Biquad(b0, b1, b2, a1, a2)
    return filt.process_block(data)


if __name__ == "__main__":
    import math as m
    fs = 100.0
    t = [i / fs for i in range(100)]
    x = [m.sin(2 * m.pi * 5 * ti) + m.sin(2 * m.pi * 30 * ti) for ti in t]
    y = butterworth_lowpass(x, 10.0, fs)
    assert len(y) == len(x)
    print("butterworth self-tests passed")
