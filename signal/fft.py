"""Cooley-Tukey Radix-2 Fast Fourier Transform.

Complexity: O(n log n). Original recursive implementation.
"""
from __future__ import annotations
import cmath
import math
from typing import List

def _fft(x: List[complex]) -> List[complex]:
    n = len(x)
    if n <= 1:
        return x
    if n & (n - 1) != 0:
        raise ValueError("Length must be a power of 2")
    even = _fft(x[0::2])
    odd = _fft(x[1::2])
    t = [cmath.exp(-2j * math.pi * k / n) * odd[k] for k in range(n // 2)]
    return [even[k] + t[k] for k in range(n // 2)] + [even[k] - t[k] for k in range(n // 2)]

def _ifft(X: List[complex]) -> List[complex]:
    n = len(X)
    conjugated = [z.conjugate() for z in X]
    y = _fft(conjugated)
    return [z.conjugate() / n for z in y]

def fft(signal: List[float]) -> List[complex]:
    n = len(signal)
    p2 = 1
    while p2 < n:
        p2 *= 2
    padded = [complex(v, 0.0) for v in signal] + [0j] * (p2 - n)
    return _fft(padded)

def ifft(spectrum: List[complex]) -> List[float]:
    y = _ifft(spectrum)
    return [z.real for z in y]

if __name__ == "__main__":
    impulse = [1.0] + [0.0] * 7
    spec = fft(impulse)
    assert len(spec) == 8
    mags = [abs(z) for z in spec]
    assert max(mags) - min(mags) < 1e-10
    recovered = ifft(spec)
    assert abs(recovered[0] - 1.0) < 1e-10
    assert all(abs(v) < 1e-10 for v in recovered[1:])
    n = 32
    freq = 3
    sine = [math.sin(2 * math.pi * freq * k / n) for k in range(n)]
    spec2 = fft(sine)
    mags2 = [abs(z) for z in spec2]
    peak = max(range(n // 2), key=lambda i: mags2[i])
    assert peak == freq, peak
    print("fft self-tests passed")
