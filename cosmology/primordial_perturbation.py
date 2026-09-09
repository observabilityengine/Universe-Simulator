"""Primordial density perturbations – power spectrum and Gaussian random field."""
from __future__ import annotations
import math
import random
from typing import List


def power_spectrum_bbks(k: float, ns: float = 0.96, sigma8: float = 0.8, h: float = 0.7) -> float:
    if k < 1e-10:
        return 0.0
    q = k / (h * 0.2)
    T = math.log(1 + 2.34 * q) / (2.34 * q)
    T /= (1 + 3.89 * q + (16.1 * q) ** 2 + (5.46 * q) ** 3 + (6.71 * q) ** 4) ** 0.25
    return k ** ns * T * T


def gaussian_random_field_1d(n: int, box_size: float, ns: float = 0.96, seed: int = 42) -> List[float]:
    rng = random.Random(seed)
    re = [0.0] * n
    im = [0.0] * n
    for i in range(1, n // 2):
        k = 2 * math.pi * i / box_size
        amp = math.sqrt(max(power_spectrum_bbks(k, ns), 0) / 2)
        re[i] = rng.gauss(0, amp)
        im[i] = rng.gauss(0, amp)
        re[n - i] = re[i]
        im[n - i] = -im[i]
    field = []
    for j in range(n):
        s = 0.0
        for i in range(n):
            angle = 2 * math.pi * i * j / n
            s += re[i] * math.cos(angle) - im[i] * math.sin(angle)
        field.append(s / n)
    return field


if __name__ == "__main__":
    pk = power_spectrum_bbks(0.1)
    assert pk > 0
    field = gaussian_random_field_1d(64, 100.0)
    assert len(field) == 64
    mean = sum(field) / len(field)
    assert abs(mean) < 0.5
    print(f"primordial_perturbation P(0.1)={pk:.4e} field_mean={mean:.3f}")
    print("primordial_perturbation self-tests passed")
