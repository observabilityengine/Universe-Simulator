"""Linear Quadratic Gaussian (LQG) controller for 1D discrete system.

Complexity: O(horizon * state_dim^3) simplified 1D. Original implementation.
Combines Kalman filter + LQR for scalar plant.
"""
from __future__ import annotations

from typing import List, Tuple


def lqr_gain(A: float, B: float, Q: float, R: float, N: int = 50) -> float:
    """Finite-horizon LQR gain for scalar system (last gain)."""
    P = Q
    for _ in range(N):
        K = (B * P * A) / (R + B * P * B)
        P = Q + A * P * A - K * (B * P * A)
    K = (B * P * A) / (R + B * P * B + 1e-15)
    return K


def kalman_gain(A: float, C: float, Q_proc: float, R_meas: float, N: int = 50) -> float:
    """Steady-ish Kalman gain for scalar system."""
    P = 1.0
    for _ in range(N):
        P_pred = A * P * A + Q_proc
        K = P_pred * C / (C * P_pred * C + R_meas + 1e-15)
        P = (1 - K * C) * P_pred
    return K


class LQG1D:
    """1D LQG: estimate state with Kalman, apply LQR feedback."""

    def __init__(
        self,
        A: float = 1.0,
        B: float = 1.0,
        C: float = 1.0,
        Q_lqr: float = 1.0,
        R_lqr: float = 0.1,
        Q_proc: float = 0.01,
        R_meas: float = 0.1,
    ):
        self.A = A
        self.B = B
        self.C = C
        self.K_lqr = lqr_gain(A, B, Q_lqr, R_lqr)
        self.K_kf = kalman_gain(A, C, Q_proc, R_meas)
        self.x_hat = 0.0

    def step(self, y: float, x_ref: float = 0.0) -> Tuple[float, float]:
        """
        Process measurement y, return (control u, state estimate).
        """
        # Kalman update
        innov = y - self.C * self.x_hat
        self.x_hat = self.x_hat + self.K_kf * innov
        # LQR control
        u = -self.K_lqr * (self.x_hat - x_ref)
        # Predict
        self.x_hat = self.A * self.x_hat + self.B * u
        return u, self.x_hat


if __name__ == "__main__":
    # Stabilize integrator-like plant
    ctrl = LQG1D(A=1.0, B=0.1, C=1.0, Q_lqr=10.0, R_lqr=0.1)
    x = 5.0
    for _ in range(100):
        y = x + 0.01  # noisy meas approx
        u, xh = ctrl.step(y)
        x = 1.0 * x + 0.1 * u
    assert abs(x) < 1.0
    assert abs(ctrl.K_lqr) > 0
    print("lqg self-tests passed")
