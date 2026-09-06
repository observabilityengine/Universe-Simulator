"""Discrete PID controller step function.

Complexity: O(1) per update.
Positional form with optional clamp on output and integral. Original implementation.
"""
from __future__ import annotations

from typing import Optional, Tuple


class PID:
    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        dt: float = 1.0,
        output_limits: Optional[Tuple[float, float]] = None,
        integral_limits: Optional[Tuple[float, float]] = None,
    ) -> None:
        self.kp, self.ki, self.kd = kp, ki, kd
        self.dt = dt
        self.output_limits = output_limits
        self.integral_limits = integral_limits
        self._integral = 0.0
        self._prev_error = 0.0
        self._first = True

    def update(self, setpoint: float, measurement: float) -> float:
        error = setpoint - measurement
        self._integral += error * self.dt
        if self.integral_limits:
            lo, hi = self.integral_limits
            self._integral = max(lo, min(hi, self._integral))
        derivative = 0.0 if self._first else (error - self._prev_error) / self.dt
        self._first = False
        self._prev_error = error
        output = self.kp * error + self.ki * self._integral + self.kd * derivative
        if self.output_limits:
            lo, hi = self.output_limits
            output = max(lo, min(hi, output))
        return output

    def reset(self) -> None:
        self._integral = 0.0
        self._prev_error = 0.0
        self._first = True


if __name__ == "__main__":
    pid = PID(1.0, 0.1, 0.05, dt=0.1, output_limits=(-10, 10))
    u = pid.update(10.0, 0.0)
    assert u > 0
    # drive toward setpoint
    x = 0.0
    for _ in range(100):
        u = pid.update(10.0, x)
        x += 0.1 * u
    assert abs(x - 10.0) < 1.0
    pid.reset()
    assert pid._integral == 0.0
    print("pid_step self-tests passed")
