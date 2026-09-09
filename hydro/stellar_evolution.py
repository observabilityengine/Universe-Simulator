"""Simple stellar evolution tracks – lifetime, endpoints by mass."""
from __future__ import annotations
from typing import Tuple


def main_sequence_lifetime(mass: float) -> float:
    return 10.0 * mass ** (-2.5)


def stellar_endpoint(mass: float) -> str:
    if mass < 0.08:
        return "brown_dwarf"
    if mass < 0.5:
        return "red_dwarf"
    if mass < 8.0:
        return "white_dwarf"
    if mass < 25.0:
        return "neutron_star"
    return "black_hole"


def luminosity(mass: float) -> float:
    return mass ** 3.5


def radius(mass: float) -> float:
    return mass ** 0.8


def evolve(mass: float, age: float) -> Tuple[str, float, float]:
    t_ms = main_sequence_lifetime(mass)
    if age < t_ms:
        return "main_sequence", luminosity(mass), radius(mass)
    if mass < 8:
        return "white_dwarf", 0.01 * luminosity(mass), 0.01 * radius(mass)
    if age < t_ms * 1.1:
        return "supernova", 1e6, 10.0
    return stellar_endpoint(mass), 0.0, 0.0


if __name__ == "__main__":
    assert stellar_endpoint(1.0) == "white_dwarf"
    assert stellar_endpoint(15.0) == "neutron_star"
    assert stellar_endpoint(40.0) == "black_hole"
    phase, L, R = evolve(1.0, 1.0)
    assert phase == "main_sequence"
    print(f"stellar_evolution 1Msun @1Gyr: {phase} L={L:.2f}")
    print("stellar_evolution self-tests passed")
