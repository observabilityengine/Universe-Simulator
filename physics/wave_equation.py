"""1D wave equation via finite differences (leapfrog).

Complexity: O(steps * n). Original implementation.
"""
from __future__ import annotations
from typing import List

def wave_equation(
    u0: List[float],
    v0: List[float] | None = None,
    c: float = 1.0,
    dx: float = 1.0,
    dt: float = 0.5,
    steps: int = 50,
) -> List[float]:
    n = len(u0)
    if v0 is None:
        v0 = [0.0] * n
    r = (c * dt / dx) ** 2
    if r > 1.0:
        raise ValueError("CFL condition violated: c*dt/dx <= 1")
    u_prev = u0[:]
    u = [0.0] * n
    for i in range(1, n - 1):
        u[i] = u0[i] + dt * v0[i] + 0.5 * r * (u0[i + 1] - 2 * u0[i] + u0[i - 1])
    u[0] = u0[0]
    u[-1] = u0[-1]
    for _ in range(steps - 1):
        u_next = [0.0] * n
        for i in range(1, n - 1):
            u_next[i] = 2 * u[i] - u_prev[i] + r * (u[i + 1] - 2 * u[i] + u[i - 1])
        u_next[0] = u0[0]
        u_next[-1] = u0[-1]
        u_prev, u = u, u_next
    return u

if __name__ == "__main__":
    n = 51
    u0 = [0.0] * n
    u0[25] = 1.0
    u = wave_equation(u0, c=1.0, dx=1.0, dt=0.5, steps=20)
    assert len(u) == n
    assert u[25] < 1.0
    assert max(u) > 0.1
    print("wave_equation self-tests passed")
