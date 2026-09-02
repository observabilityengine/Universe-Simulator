"""
Universe Simulator - Bang-Bang (On-Off) Controller
Original hysteresis controller.
"""

from __future__ import annotations


class BangBang:
    def __init__(self, setpoint: float, hysteresis: float, output_high: float = 1.0, output_low: float = -1.0):
        self.setpoint = setpoint
        self.hyst = hysteresis
        self.high = output_high
        self.low = output_low
        self.state = 0.0

    def update(self, measurement: float) -> float:
        error = self.setpoint - measurement
        if error > self.hyst:
            self.state = self.high
        elif error < -self.hyst:
            self.state = self.low
        return self.state


if __name__ == "__main__":
    ctrl = BangBang(setpoint=0.0, hysteresis=0.5)
    assert ctrl.update(-1.0) == 1.0
    assert ctrl.update(0.0) == 1.0  # stays high until crosses -hyst the other way
    assert ctrl.update(1.0) == -1.0
    print("bang_bang self-test passed")
