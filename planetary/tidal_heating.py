"""Tidal heating – viscoelastic dissipation in satellites/planets."""
from __future__ import annotations
import math


def tidal_power(mass_primary: float, mass_secondary: float, semi_major: float, eccentricity: float, radius_secondary: float, k2: float = 0.3, Q: float = 100.0, G: float = 1.0, n_orb: float | None = None) -> float:
    if n_orb is None:
        n_orb = math.sqrt(G * (mass_primary + mass_secondary) / semi_major ** 3)
    return 21.0 / 2.0 * (k2 / Q) * G * mass_primary ** 2 * radius_secondary ** 5 * n_orb * eccentricity ** 2 / semi_major ** 6


def equilibrium_temperature(power: float, radius: float, albedo: float = 0.1, sigma_sb: float = 1.0) -> float:
    flux = power / (4 * math.pi * radius ** 2)
    return (flux / (sigma_sb * max(1 - albedo, 0.01))) ** 0.25


if __name__ == "__main__":
    P = tidal_power(1.0, 0.01, 5.0, 0.1, 0.2)
    assert P > 0
    T = equilibrium_temperature(P, 0.2)
    print(f"tidal_heating power={P:.3e} T={T:.3e}")
    print("tidal_heating self-tests passed")
