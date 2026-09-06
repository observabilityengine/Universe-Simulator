"""Cooley-Tukey radix-2 FFT (iterative).

Complexity: O(n log n) for n power of 2.
Computes discrete Fourier transform. Input length must be power of 2.
"""
from __future__ import annotations

import cmath
from typing import List
import numpy as np


def fft(x: List[complex]) -> List[complex]:
    """Forward FFT. Length must be power of 2."""
    n = len(x)
    if n == 0:
        return []
    if n & (n - 1) != 0:
        raise ValueError("length must be power of 2")
    a = list(x)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = cmath.exp(-2j * cmath.pi / length)
        for i in range(0, n, length):
            w = 1 + 0j
            for j in range(length // 2):
                u = a[i + j]
                v = a[i + j + length // 2] * w
                a[i + j] = u + v
                a[i + j + length // 2] = u - v
                w *= wlen
        length <<= 1
    return a


def ifft(X: List[complex]) -> List[complex]:
    """Inverse FFT (normalized)."""
    n = len(X)
    conj = [z.conjugate() for z in X]
    y = fft(conj)
    return [z.conjugate() / n for z in y]


if __name__ == "__main__":
    x = [1 + 0j] + [0j] * 7
    X = fft(x)
    assert all(abs(z - 1) < 1e-10 for z in X)
    x2 = [complex(i, 0) for i in range(8)]
    X2 = fft(x2)
    y2 = ifft(X2)
    assert all(abs(a - b) < 1e-10 for a, b in zip(x2, y2))
    assert fft([]) == []
    try:
        fft([1, 2, 3])
        assert False
    except ValueError:
        pass
    x3 = np.random.randn(16) + 1j * np.random.randn(16)
    X3 = fft(list(x3))
    npX = np.fft.fft(x3)
    assert np.allclose(X3, npX, atol=1e-8)
    print("fft self-tests passed")
