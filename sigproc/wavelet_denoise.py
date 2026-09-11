"""Haar wavelet soft-threshold denoising."""
from __future__ import annotations
from typing import List
from .wavelet import haar_forward, haar_inverse, haar_multilevel


def soft_threshold(coeffs: List[float], t: float) -> List[float]:
    return [0.0 if abs(c) <= t else (c - t if c > 0 else c + t) for c in coeffs]


def wavelet_denoise(x: List[float], threshold: float = 0.5, levels: int = 2) -> List[float]:
    # single-level for simplicity with reconstruct
    current = list(x)
    details = []
    for _ in range(levels):
        if len(current) < 2:
            break
        approx, detail = haar_forward(current)
        details.append(soft_threshold(detail, threshold))
        current = approx
    # reconstruct
    for detail in reversed(details):
        # pad lengths if needed
        m = min(len(current), len(detail))
        current = haar_inverse(current[:m], detail[:m])
    return current[: len(x)]


if __name__ == "__main__":
    import random
    rng = random.Random(0)
    clean = [float(i % 5) for i in range(32)]
    noisy = [c + rng.gauss(0, 0.3) for c in clean]
    denoised = wavelet_denoise(noisy, threshold=0.4, levels=2)
    assert len(denoised) == len(clean)
    print(f"wavelet_denoise len={len(denoised)}")
    print("wavelet_denoise self-tests passed")
