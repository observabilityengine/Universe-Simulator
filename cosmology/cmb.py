"""CMB temperature anisotropy – simplified angular power spectrum and map."""
from __future__ import annotations
import math
import random
from typing import List


def cl_spectrum(l_max: int = 50, A: float = 1.0, ns: float = 0.96) -> List[float]:
    cls = [0.0]
    for ell in range(1, l_max + 1):
        base = A / (ell * (ell + 1)) * (ell ** (ns - 1))
        peak = 1 + 2 * math.exp(-0.5 * ((ell - 220) / 50) ** 2) if ell < l_max else 1
        cls.append(base * peak)
    return cls


def generate_temperature_map(n_theta: int = 36, n_phi: int = 72, l_max: int = 20, seed: int = 42) -> List[List[float]]:
    rng = random.Random(seed)
    cls = cl_spectrum(l_max)
    alm = {}
    for ell in range(1, l_max + 1):
        for m in range(-ell, ell + 1):
            sigma = math.sqrt(cls[ell] / 2)
            alm[(ell, m)] = complex(rng.gauss(0, sigma), rng.gauss(0, sigma))
    grid = [[0.0] * n_phi for _ in range(n_theta)]
    for i in range(n_theta):
        theta = math.pi * (i + 0.5) / n_theta
        for j in range(n_phi):
            phi = 2 * math.pi * j / n_phi
            t = 0.0
            for ell in range(1, min(l_max, 10) + 1):
                for m in range(0, ell + 1):
                    a = alm[(ell, m)]
                    y = math.cos(m * phi) * (math.sin(theta) ** abs(m)) * math.cos(ell * theta)
                    t += a.real * y
            grid[i][j] = t
    return grid


if __name__ == "__main__":
    cls = cl_spectrum(30)
    assert cls[2] > 0
    mp = generate_temperature_map(18, 36, l_max=8)
    assert len(mp) == 18
    print(f"cmb C_2={cls[2]:.4e} map={len(mp)}x{len(mp[0])}")
    print("cmb self-tests passed")
