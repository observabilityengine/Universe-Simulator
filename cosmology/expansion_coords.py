"""Comoving / proper coordinate transforms and peculiar velocities."""
from __future__ import annotations


def comoving_to_proper(x_comoving: float, a: float) -> float:
    return a * x_comoving


def proper_to_comoving(x_proper: float, a: float) -> float:
    return x_proper / a


def peculiar_velocity(v_physical: float, a: float, H: float, x_comoving: float) -> float:
    return v_physical - a * H * x_comoving


def physical_velocity(v_peculiar: float, a: float, H: float, x_comoving: float) -> float:
    return v_peculiar + a * H * x_comoving


def redshift_to_scale(z: float) -> float:
    return 1.0 / (1.0 + z)


def scale_to_redshift(a: float) -> float:
    return 1.0 / a - 1.0


if __name__ == "__main__":
    a = 0.5
    assert abs(comoving_to_proper(2.0, a) - 1.0) < 1e-12
    assert abs(scale_to_redshift(0.5) - 1.0) < 1e-12
    print("expansion_coords self-tests passed")
