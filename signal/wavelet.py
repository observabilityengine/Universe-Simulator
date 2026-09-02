"""
Universe Simulator - Haar Wavelet Transform (1-D)
Original in-place Haar decomposition / reconstruction.
"""

from __future__ import annotations

from typing import List


def haar_forward(data: List[float]) -> List[float]:
    n = len(data)
    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError("length must be power of 2")
    out = data[:]
    temp = [0.0] * n
    length = n
    while length > 1:
        half = length // 2
        for i in range(half):
            avg = (out[2 * i] + out[2 * i + 1]) / 2.0
            diff = (out[2 * i] - out[2 * i + 1]) / 2.0
            temp[i] = avg
            temp[half + i] = diff
        out[:length] = temp[:length]
        length = half
    return out


def haar_inverse(coeffs: List[float]) -> List[float]:
    n = len(coeffs)
    out = coeffs[:]
    temp = [0.0] * n
    length = 1
    while length < n:
        half = length
        length *= 2
        for i in range(half):
            avg = out[i]
            diff = out[half + i]
            temp[2 * i] = avg + diff
            temp[2 * i + 1] = avg - diff
        out[:length] = temp[:length]
    return out


if __name__ == "__main__":
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    c = haar_forward(x)
    rec = haar_inverse(c)
    assert all(abs(a - b) < 1e-9 for a, b in zip(x, rec))
    print("wavelet self-test passed", c)
