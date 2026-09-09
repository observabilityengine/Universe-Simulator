"""Zero-dimensional climate / energy-balance model."""
from __future__ import annotations
import math


def equilibrium_temperature(stellar_flux: float, albedo: float = 0.3, sigma_sb: float = 5.67e-8, greenhouse_factor: float = 1.0) -> float:
    return (stellar_flux * (1 - albedo) / (4 * sigma_sb * greenhouse_factor)) ** 0.25


def energy_balance_step(T: float, stellar_flux: float, albedo: float, heat_capacity: float, dt: float, sigma_sb: float = 5.67e-8, greenhouse: float = 0.6) -> float:
    incoming = stellar_flux * (1 - albedo) / 4
    outgoing = greenhouse * sigma_sb * T ** 4
    return T + dt * (incoming - outgoing) / heat_capacity


def run_climate(T0: float = 288.0, stellar_flux: float = 1361.0, albedo: float = 0.3, n_steps: int = 500, dt: float = 1e6) -> float:
    T = T0
    for _ in range(n_steps):
        T = energy_balance_step(T, stellar_flux, albedo, heat_capacity=1e8, dt=dt)
    return T


if __name__ == "__main__":
    Teq = equilibrium_temperature(1361.0, 0.3, greenhouse_factor=0.6)
    assert 200 < Teq < 400
    T = run_climate()
    print(f"climate_energy Teq={Teq:.1f}K evolved={T:.1f}K")
    print("climate_energy self-tests passed")
