"""Keplerian orbital period and circular orbit velocity.

Complexity: O(1).
Uses μ = GM. Original implementation.
"""
from __future__ import annotations

import math

# Standard gravitational parameter for Earth (m^3/s^2)
MU_EARTH = 3.986004418e14


def orbital_period(a: float, mu: float = MU_EARTH) -> float:
    """Sidereal period for semi-major axis a (meters)."""
    if a <= 0 or mu <= 0:
        raise ValueError("a and mu must be positive")
    return 2 * math.pi * math.sqrt(a**3 / mu)


def circular_velocity(r: float, mu: float = MU_EARTH) -> float:
    """Circular orbit speed at radius r."""
    if r <= 0 or mu <= 0:
        raise ValueError("r and mu must be positive")
    return math.sqrt(mu / r)


def escape_velocity(r: float, mu: float = MU_EARTH) -> float:
    if r <= 0 or mu <= 0:
        raise ValueError("r and mu must be positive")
    return math.sqrt(2 * mu / r)


if __name__ == "__main__":
    # LEO ~ 6771 km radius → period ~ 92 min
    T = orbital_period(6.771e6)
    assert 5000 < T < 6000
    v = circular_velocity(6.771e6)
    assert 7000 < v < 8000
    assert escape_velocity(6.771e6) > v
    print("orbital_period self-tests passed")
