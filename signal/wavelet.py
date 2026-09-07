"""Haar discrete wavelet transform (1D).

Complexity: O(n). Original implementation.
"""
from __future__ import annotations
import math
from typing import List, Tuple

def haar_forward(signal: List[float]) -> Tuple[List[float], List[List[float]]]:
    x = signal[:]
    details: List[List[float]] = []
    while len(x) >= 2:
        n = len(x) - (len(x) % 2)
        approx = []
        detail = []
        for i in range(0, n, 2):
            a = (x[i] + x[i + 1]) / math.sqrt(2)
            d = (x[i] - x[i + 1]) / math.sqrt(2)
            approx.append(a)
            detail.append(d)
        details.append(detail)
        x = approx
    return x, details

def haar_inverse(approx: List[float], details: List[List[float]]) -> List[float]:
    x = approx[:]
    for detail in reversed(details):
        out = []
        for a, d in zip(x, detail):
            out.append((a + d) / math.sqrt(2))
            out.append((a - d) / math.sqrt(2))
        x = out
    return x

if __name__ == "__main__":
    sig = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    approx, details = haar_forward(sig)
    recovered = haar_inverse(approx, details)
    assert len(recovered) == len(sig)
    assert all(abs(a - b) < 1e-10 for a, b in zip(sig, recovered))
    e1 = sum(v * v for v in sig)
    e2 = sum(v * v for v in approx) + sum(sum(d * d for d in lev) for lev in details)
    assert abs(e1 - e2) < 1e-8
    print("wavelet self-tests passed")
