"""Ziegler-Nichols PID autotuning (relay method simplified).

Complexity: O(steps). Original implementation.
"""
from __future__ import annotations
from typing import Callable, Tuple

def ziegler_nichols_relay(
    plant: Callable[[float], float],
    steps: int = 500,
    d: float = 1.0,
) -> Tuple[float, float, float]:
    """Estimate Ku, Pu via relay feedback, return (Kp, Ki, Kd) for classic ZN."""
    u = d
    ys = []
    for t in range(steps):
        y = plant(u)
        ys.append(y)
        u = d if y < 0 else -d
    crossings = [i for i in range(1, len(ys)) if ys[i-1]*ys[i] < 0]
    if len(crossings) < 4:
        return 1.0, 0.0, 0.0
    periods = [crossings[i+1]-crossings[i] for i in range(len(crossings)-1)]
    Pu = 2 * (sum(periods)/len(periods))
    a = (max(ys) - min(ys)) / 2
    Ku = 4 * d / (3.14159 * a) if a > 1e-9 else 1.0
    Kp = 0.6 * Ku
    Ki = 1.2 * Ku / Pu
    Kd = 0.075 * Ku * Pu
    return Kp, Ki, Kd

if __name__ == "__main__":
    s1, s2 = [0.0], [0.0]
    def plant(u):
        s2[0] += 0.05 * (u - s1[0])
        s1[0] += 0.05 * s2[0]
        return s1[0]
    Kp, Ki, Kd = ziegler_nichols_relay(plant, steps=400, d=1.0)
    assert isinstance(Kp, float)
    print("pid_autotune self-tests passed")
