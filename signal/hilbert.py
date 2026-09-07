"""Hilbert transform via FFT for analytic signal.

Complexity: O(n log n). Original implementation.
"""
from __future__ import annotations
from typing import List
import cmath
import math

def _fft(x):
    n = len(x)
    if n <= 1: return x
    even = _fft(x[0::2])
    odd = _fft(x[1::2])
    t = [cmath.exp(-2j*math.pi*k/n)*odd[k] for k in range(n//2)]
    return [even[k]+t[k] for k in range(n//2)] + [even[k]-t[k] for k in range(n//2)]

def _ifft(X):
    n = len(X)
    conj = [z.conjugate() for z in X]
    y = _fft(conj)
    return [z.conjugate()/n for z in y]

def hilbert(signal: List[float]) -> List[complex]:
    n = len(signal)
    p2 = 1
    while p2 < n: p2 *= 2
    padded = [complex(v) for v in signal] + [0j]*(p2-n)
    X = _fft(padded)
    h = [0.0]*p2
    h[0] = 1.0
    if p2 > 1:
        h[p2//2] = 1.0
    for i in range(1, p2//2):
        h[i] = 2.0
    Xh = [X[i]*h[i] for i in range(p2)]
    analytic = _ifft(Xh)
    return analytic[:n]

if __name__ == "__main__":
    n = 32
    sig = [math.cos(2*math.pi*3*k/n) for k in range(n)]
    ana = hilbert(sig)
    imag = [z.imag for z in ana]
    sine = [math.sin(2*math.pi*3*k/n) for k in range(n)]
    err = sum((imag[i]-sine[i])**2 for i in range(n))/n
    assert err < 0.1, err
    print("hilbert self-tests passed")
