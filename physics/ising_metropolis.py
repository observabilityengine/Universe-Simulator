"""2-D Ising model Metropolis Monte Carlo.

Complexity: O(steps * L^2).
Periodic boundaries. Returns final spins, energy density, |magnetization|.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def ising_metropolis(
    L: int,
    T: float,
    steps: int,
    J: float = 1.0,
    seed: int | None = None,
) -> Tuple[np.ndarray, float, float]:
    """Run Metropolis on LxL Ising lattice.

    Returns (final_spins, energy_per_site, magnetization_per_site).
    """
    if L < 1 or steps < 0:
        raise ValueError("invalid L or steps")
    rng = np.random.default_rng(seed)
    spins = rng.choice([-1, 1], size=(L, L))
    beta = 1.0 / T if T > 0 else np.inf

    def energy():
        e = 0.0
        for i in range(L):
            for j in range(L):
                e -= J * spins[i, j] * spins[i, (j + 1) % L]
                e -= J * spins[i, j] * spins[(i + 1) % L, j]
        return e

    for _ in range(steps):
        i = rng.integers(0, L)
        j = rng.integers(0, L)
        s = spins[i, j]
        nn = (
            spins[i, (j + 1) % L]
            + spins[i, (j - 1) % L]
            + spins[(i + 1) % L, j]
            + spins[(i - 1) % L, j]
        )
        dE = 2 * J * s * nn
        if dE <= 0 or rng.random() < np.exp(-beta * dE):
            spins[i, j] = -s

    e = energy() / (L * L)
    m = abs(spins.mean())
    return spins, e, m


if __name__ == "__main__":
    spins, e, m = ising_metropolis(4, 1.0, 100, seed=42)
    assert spins.shape == (4, 4)
    assert -2.1 < e < 2.1
    assert 0 <= m <= 1
    _, _, m_low = ising_metropolis(8, 0.1, 2000, seed=1)
    assert m_low > 0.5
    s0, e0, m0 = ising_metropolis(2, 1.0, 0, seed=0)
    assert s0.shape == (2, 2)
    try:
        ising_metropolis(0, 1.0, 10)
        assert False
    except ValueError:
        pass
    print("ising_metropolis self-tests passed")
