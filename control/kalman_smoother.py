"""Rauch-Tung-Striebel Kalman smoother.

Complexity: O(T n^3). Original implementation.
"""
from __future__ import annotations
from typing import List

def kalman_smoother(
    ys: List[float],
    A: float = 1.0,
    C: float = 1.0,
    Q: float = 0.1,
    R: float = 1.0,
    x0: float = 0.0,
    P0: float = 1.0,
) -> List[float]:
    """1D RTS smoother. Returns smoothed state estimates."""
    T = len(ys)
    x_f = [0.0] * T
    P_f = [0.0] * T
    x_p = [0.0] * T
    P_p = [0.0] * T
    x, P = x0, P0
    for t in range(T):
        x_pred = A * x
        P_pred = A * P * A + Q
        K = P_pred * C / (C * P_pred * C + R)
        x = x_pred + K * (ys[t] - C * x_pred)
        P = (1 - K * C) * P_pred
        x_f[t], P_f[t] = x, P
        x_p[t], P_p[t] = x_pred, P_pred
    x_s = [0.0] * T
    x_s[-1] = x_f[-1]
    for t in range(T - 2, -1, -1):
        J = P_f[t] * A / P_p[t + 1] if P_p[t + 1] > 1e-15 else 0.0
        x_s[t] = x_f[t] + J * (x_s[t + 1] - x_p[t + 1])
    return x_s

if __name__ == "__main__":
    true = [1.0] * 20
    import random
    rng = random.Random(1)
    ys = [t + rng.gauss(0, 0.5) for t in true]
    sm = kalman_smoother(ys, Q=0.01, R=0.25)
    mse_raw = sum((y - 1)**2 for y in ys) / 20
    mse_sm = sum((s - 1)**2 for s in sm) / 20
    assert mse_sm < mse_raw
    print("kalman_smoother self-tests passed")
