"""
Universe Simulator - SABR Implied Volatility
Original Hagan approximation for SABR model.
"""

from __future__ import annotations

import math

def sabr_implied_vol(F: float, K: float, T: float, alpha: float, beta: float, rho: float, nu: float) -> float:
    if F <= 0 or K <= 0 or T <= 0:
        return 0.0
    if abs(F - K) < 1e-12:
        # ATM
        return alpha / (F ** (1 - beta)) * (1 + ((1-beta)**2 / 24 * alpha**2 / F**(2-2*beta) + 0.25 * rho * beta * nu * alpha / F**(1-beta) + (2-3*rho**2)/24 * nu**2) * T)
    FK = F * K
    logFK = math.log(F / K)
    z = (nu / alpha) * (FK ** ((1-beta)/2)) * logFK
    xz = math.log((math.sqrt(1 - 2*rho*z + z*z) + z - rho) / (1 - rho))
    A = alpha / ((FK)**((1-beta)/2) * (1 + (1-beta)**2 / 24 * logFK**2 + (1-beta)**4 / 1920 * logFK**4))
    B = 1 + ((1-beta)**2 / 24 * alpha**2 / (FK)**(1-beta) + 0.25 * rho * beta * nu * alpha / (FK)**((1-beta)/2) + (2-3*rho**2)/24 * nu**2) * T
    return A * z / xz * B

if __name__ == "__main__":
    vol = sabr_implied_vol(100, 100, 1.0, 0.3, 0.5, -0.2, 0.4)
    assert 0.1 < vol < 1.0
    print("sabr self-test passed", vol)
