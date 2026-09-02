"""
Module 13 – PID Controller
Full proportional-integral-derivative controller with anti-windup.
Original, executable implementation.
"""

from __future__ import annotations
from typing import Optional


class PIDController:
    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        setpoint: float = 0.0,
        output_limits: tuple[float, float] = (-float("inf"), float("inf")),
        integral_limits: tuple[float, float] = (-float("inf"), float("inf")),
        sample_time: float = 0.01,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self._min_out, self._max_out = output_limits
        self._min_int, self._max_int = integral_limits
        self.sample_time = sample_time
        self._integral = 0.0
        self._last_error = 0.0
        self._last_output = 0.0

    def update(self, measurement: float, dt: Optional[float] = None) -> float:
        error = self.setpoint - measurement
        if dt is None:
            dt = self.sample_time
        if dt <= 0.0:
            return self._last_output
        p = self.kp * error
        self._integral += error * dt
        self._integral = max(self._min_int, min(self._max_int, self._integral))
        i = self.ki * self._integral
        d = self.kd * (error - self._last_error) / dt
        output = p + i + d
        output = max(self._min_out, min(self._max_out, output))
        self._last_error = error
        self._last_output = output
        return output

    def reset(self) -> None:
        self._integral = 0.0
        self._last_error = 0.0
        self._last_output = 0.0


if __name__ == "__main__":
    print("Testing PID Controller...")
    pid = PIDController(kp=2.0, ki=1.0, kd=0.05, setpoint=10.0, output_limits=(-5, 5))
    x = 0.0
    dt = 0.05
    for step in range(80):
        u = pid.update(x, dt)
        x += u * dt
        if step % 20 == 0:
            print(f"  t={step*dt:.1f}  x={x:.3f}  u={u:.3f}")
    print(f"Final x={x:.3f} (target 10.0)")
    print("PID Controller module OK.")
