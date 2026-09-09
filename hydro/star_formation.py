"""Star formation – density threshold, efficiency, stellar particle creation."""
from __future__ import annotations
import math
import random
from typing import List, Tuple


def star_formation_rate(rho: float, free_fall_factor: float = 0.01, rho_thresh: float = 1.0, t_ff_coeff: float = 1.0) -> float:
    if rho < rho_thresh:
        return 0.0
    t_ff = t_ff_coeff / math.sqrt(rho)
    return free_fall_factor * rho / t_ff


def create_star_particles(gas_masses: List[float], gas_densities: List[float], dt: float, rho_thresh: float = 1.0, efficiency: float = 0.01, seed: int = 42) -> List[Tuple[int, float]]:
    rng = random.Random(seed)
    formed = []
    for i, (m, rho) in enumerate(zip(gas_masses, gas_densities)):
        sfr = star_formation_rate(rho, efficiency, rho_thresh)
        m_star = sfr * dt * (m / max(rho, 1e-30))
        if m_star > 0 and rng.random() < min(1.0, m_star / m):
            formed.append((i, min(m_star, 0.5 * m)))
    return formed


if __name__ == "__main__":
    sfr = star_formation_rate(10.0, rho_thresh=1.0)
    assert sfr > 0
    assert star_formation_rate(0.1, rho_thresh=1.0) == 0.0
    formed = create_star_particles([1, 1], [10, 0.1], dt=0.1, seed=1)
    print(f"star_formation sfr={sfr:.4f} formed={formed}")
    print("star_formation self-tests passed")
