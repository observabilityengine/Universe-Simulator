"""1D heat equation via explicit finite differences.

Complexity: O(steps * n). Original implementation.
"""
from __future__ import annotations
from typing import List

def heat_equation(
    u0: List[float],
    alpha: float = 0.01,
    dx: float = 1.0,
    dt: float = 0.1,
    steps: int = 100,
) -> List[float]:
    r = alpha * dt / (dx * dx)
    if r > 0.5:
        raise ValueError("Unstable: need alpha*dt/dx^2 <= 0.5")
    u = u0[:]
    n = len(u)
    for _ in range(steps):
        new = u[:]
        for i in range(1, n-1):
            new[i] = u[i] + r * (u[i+1] - 2*u[i] + u[i-1])
        u = new
    return u

if __name__ == "__main__":
    u0 = [0.0]*21
    u0[10] = 1.0
    u = heat_equation(u0, alpha=0.25, dx=1.0, dt=0.5, steps=20)
    assert u[10] < 1.0
    assert u[10] > u[0]
    assert all(v >= -1e-9 for v in u)
    print("heat_equation self-tests passed")
