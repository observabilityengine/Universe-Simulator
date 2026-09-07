"""2D Ising model Monte Carlo (Metropolis).

Complexity: O(steps * L^2). Original implementation.
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple

def ising_metropolis(
    L: int = 20, temperature: float = 2.2, steps: int = 5000,
    J: float = 1.0, seed: int = 42,
) -> Tuple[List[List[int]], float, float]:
    rng = random.Random(seed)
    spins = [[1 if rng.random() < 0.5 else -1 for _ in range(L)] for _ in range(L)]
    beta = 1.0 / max(temperature, 1e-12)

    def energy() -> float:
        E = 0.0
        for i in range(L):
            for j in range(L):
                s = spins[i][j]
                E -= J * s * spins[i][(j + 1) % L]
                E -= J * s * spins[(i + 1) % L][j]
        return E

    def magnetization() -> float:
        return sum(sum(row) for row in spins) / (L * L)

    E = energy()
    energy_acc = mag_acc = sample_count = 0.0
    thermal = steps // 5
    for step in range(steps):
        i = rng.randrange(L)
        j = rng.randrange(L)
        s = spins[i][j]
        nn = (spins[i][(j+1)%L] + spins[i][(j-1)%L] + spins[(i+1)%L][j] + spins[(i-1)%L][j])
        dE = 2 * J * s * nn
        if dE <= 0 or rng.random() < math.exp(-beta * dE):
            spins[i][j] = -s
            E += dE
        if step >= thermal:
            energy_acc += E
            mag_acc += abs(magnetization())
            sample_count += 1
    mean_E = energy_acc / sample_count / (L * L) if sample_count else 0.0
    mean_M = mag_acc / sample_count if sample_count else 0.0
    return spins, mean_E, mean_M

if __name__ == "__main__":
    _, e_low, m_low = ising_metropolis(L=16, temperature=0.8, steps=15000, seed=1)
    _, e_high, m_high = ising_metropolis(L=16, temperature=8.0, steps=15000, seed=2)
    assert e_low < e_high
    assert e_low < -1.0
    assert e_high > -0.8
    assert 0.0 <= m_low <= 1.0
    print("ising self-tests passed")
