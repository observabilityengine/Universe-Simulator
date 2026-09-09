"""Friedmann equation solver – scale factor evolution, cosmic age, distances."""
from __future__ import annotations
import math
from typing import List, Tuple


def hubble(a: float, Om: float = 0.3, Or: float = 0.0, Ol: float = 0.7, H0: float = 70.0) -> float:
    Ok = 1.0 - Om - Or - Ol
    return H0 * math.sqrt(Or / a**4 + Om / a**3 + Ok / a**2 + Ol)


def dadt(a: float, Om: float, Or: float, Ol: float, H0: float) -> float:
    return hubble(a, Om, Or, Ol, H0) * a / 977.8


def evolve_scale_factor(
    a0: float = 1e-4,
    a1: float = 1.0,
    Om: float = 0.3,
    Or: float = 8e-5,
    Ol: float = 0.7,
    H0: float = 70.0,
    n_steps: int = 2000,
) -> Tuple[List[float], List[float]]:
    da = (a1 - a0) / n_steps
    a = a0
    t = 0.0
    times, scales = [t], [a]
    for _ in range(n_steps):
        def f(aa):
            return 1.0 / max(dadt(aa, Om, Or, Ol, H0), 1e-30)
        k1 = f(a)
        k2 = f(a + 0.5 * da)
        k3 = f(a + 0.5 * da)
        k4 = f(a + da)
        dt = (da / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        a += da
        times.append(t)
        scales.append(a)
    return times, scales


def cosmic_age(Om: float = 0.3, Ol: float = 0.7, H0: float = 70.0, Or: float = 8e-5) -> float:
    times, _ = evolve_scale_factor(1e-5, 1.0, Om, Or, Ol, H0, n_steps=5000)
    return times[-1]


def comoving_distance(z: float, Om: float = 0.3, Ol: float = 0.7, H0: float = 70.0, n: int = 200) -> float:
    c = 299792.458
    dz = z / n
    s = 0.0
    for i in range(n):
        zi = (i + 0.5) * dz
        ai = 1.0 / (1 + zi)
        s += c / hubble(ai, Om, 0, Ol, H0)
    return s * dz


if __name__ == "__main__":
    age = cosmic_age()
    assert 12 < age < 15
    chi = comoving_distance(1.0)
    assert 3000 < chi < 4000
    print(f"friedmann age={age:.2f} Gyr chi(z=1)={chi:.0f} Mpc")
    print("friedmann self-tests passed")
