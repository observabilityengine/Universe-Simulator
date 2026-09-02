"""
Universe Simulator - Simulation Clock
Original fixed/variable timestep clock with pause and time-scale.
"""

from __future__ import annotations

import time
from typing import Optional


class SimClock:
    def __init__(self, fixed_dt: Optional[float] = None):
        self.fixed_dt = fixed_dt
        self.sim_time = 0.0
        self.real_start = time.perf_counter()
        self.paused = False
        self.time_scale = 1.0
        self._last_real = self.real_start

    def tick(self) -> float:
        """Advance and return dt used this frame."""
        now = time.perf_counter()
        if self.paused:
            self._last_real = now
            return 0.0
        real_dt = now - self._last_real
        self._last_real = now
        dt = self.fixed_dt if self.fixed_dt is not None else real_dt
        dt *= self.time_scale
        self.sim_time += dt
        return dt

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False
        self._last_real = time.perf_counter()

    def set_scale(self, scale: float) -> None:
        self.time_scale = max(0.0, scale)


if __name__ == "__main__":
    clk = SimClock(fixed_dt=0.016)
    dts = [clk.tick() for _ in range(5)]
    assert all(abs(d - 0.016) < 1e-9 for d in dts)
    assert abs(clk.sim_time - 0.08) < 1e-9
    print("clock self-test passed", clk.sim_time)
