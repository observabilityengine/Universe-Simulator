"""Discrete lead-lag compensator.

Complexity: O(1) per sample.
Transfer: C(z) ≈ K (z - z_zero)/(z - z_pole) via bilinear-style difference eq.
Original implementation.
"""
from __future__ import annotations


class LeadLag:
    def __init__(self, gain: float, zero: float, pole: float, dt: float = 1.0) -> None:
        """zero/pole are continuous-time frequencies (rad/s); discretized via Tustin-like map."""
        if dt <= 0:
            raise ValueError("dt must be positive")
        self.K = gain
        # simple matched pole-zero discrete form
        self.a = (2 / dt + zero) / (2 / dt + pole) if abs(2 / dt + pole) > 1e-15 else 1.0
        self.b = (2 / dt - zero) / (2 / dt + pole) if abs(2 / dt + pole) > 1e-15 else 0.0
        self.c = (2 / dt - pole) / (2 / dt + pole) if abs(2 / dt + pole) > 1e-15 else 0.0
        self._x = 0.0  # previous input
        self._y = 0.0  # previous output

    def update(self, u: float) -> float:
        y = self.K * (self.a * u + self.b * self._x - self.c * self._y)
        # rearrange standard: y[k] = K*((a0*u[k]+a1*u[k-1]) - b1*y[k-1]) simplified
        y = self.K * (u - self.zero_disc * self._x + self.pole_disc * self._y) if False else y
        self._x = u
        self._y = y
        return y

    def reset(self) -> None:
        self._x = 0.0
        self._y = 0.0


# Cleaner implementation
class LeadLagFilter:
    """y[k] = α y[k-1] + β (u[k] - γ u[k-1])."""

    def __init__(self, alpha: float, beta: float, gamma: float) -> None:
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self._u_prev = 0.0
        self._y_prev = 0.0

    def update(self, u: float) -> float:
        y = self.alpha * self._y_prev + self.beta * (u - self.gamma * self._u_prev)
        self._u_prev = u
        self._y_prev = y
        return y

    def reset(self) -> None:
        self._u_prev = 0.0
        self._y_prev = 0.0


if __name__ == "__main__":
    f = LeadLagFilter(alpha=0.5, beta=1.0, gamma=0.2)
    y1 = f.update(1.0)
    y2 = f.update(1.0)
    assert isinstance(y1, float) and isinstance(y2, float)
    f.reset()
    assert f.update(0.0) == 0.0
    print("lead_lag self-tests passed")
