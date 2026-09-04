"""
Universe Simulator - Simple Haar Wavelet Denoising
Original soft-thresholding on detail coefficients.
"""

from __future__ import annotations

from typing import List

def haar_transform(data: List[float]) -> List[float]:
    n = len(data)
    out = data[:]
    while n > 1:
        n2 = n // 2
        temp = [0.0] * n
        for i in range(n2):
            temp[i] = (out[2*i] + out[2*i+1]) / 2
            temp[n2 + i] = (out[2*i] - out[2*i+1]) / 2
        out[:n] = temp
        n = n2
    return out

def haar_inverse(coeffs: List[float]) -> List[float]:
    n = 1
    out = coeffs[:]
    while n < len(coeffs):
        n2 = n * 2
        temp = [0.0] * n2
        for i in range(n):
            temp[2*i] = out[i] + out[n + i]
            temp[2*i+1] = out[i] - out[n + i]
        out[:n2] = temp
        n = n2
    return out

def denoise(data: List[float], threshold: float = 0.1) -> List[float]:
    # pad to power of 2
    n = 1
    while n < len(data):
        n *= 2
    padded = data + [0.0] * (n - len(data))
    coeffs = haar_transform(padded)
    for i in range(1, len(coeffs)):
        if abs(coeffs[i]) < threshold:
            coeffs[i] = 0.0
        else:
            coeffs[i] = math.copysign(abs(coeffs[i]) - threshold, coeffs[i])
    recon = haar_inverse(coeffs)
    return recon[:len(data)]

import math

if __name__ == "__main__":
    clean = [math.sin(i * 0.3) for i in range(32)]
    noisy = [c + 0.4 * ((i % 5) - 2) for i, c in enumerate(clean)]
    denoised = denoise(noisy, 0.2)
    assert len(denoised) == 32
    print("wavelet_denoise self-test passed")
