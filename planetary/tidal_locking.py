"""Tidal locking timescale and synchronous rotation state."""
from __future__ import annotations
import math


def locking_timescale(mass_primary: float, mass_secondary: float, semi_major: float, radius_secondary: float, k2: float = 0.3, Q: float = 100.0, G: float = 1.0, omega_spin0: float | None = None) -> float:
    if omega_spin0 is None:
        omega_spin0 = math.sqrt(G * mass_primary / semi_major ** 3) * 2
    return omega_spin0 * radius_secondary ** 3 / (G * mass_primary) * (semi_major / radius_secondary) ** 6 * Q / k2


def is_tidally_locked(spin_period: float, orbital_period: float, tolerance: float = 0.05) -> bool:
    return abs(spin_period - orbital_period) / orbital_period < tolerance


def orbital_period(semi_major: float, mass_central: float, G: float = 1.0) -> float:
    return 2 * math.pi * math.sqrt(semi_major ** 3 / (G * mass_central))


if __name__ == "__main__":
    tau = locking_timescale(1.0, 0.01, 10.0, 0.3)
    assert tau > 0
    P = orbital_period(1.0, 1.0)
    assert is_tidally_locked(P, P)
    print(f"tidal_locking tau={tau:.3e}")
    print("tidal_locking self-tests passed")
