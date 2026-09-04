"""
Universe Simulator - IIR Notch Filter
Original second-order notch for removing a single frequency.
"""

from __future__ import annotations

import math
from typing import List

class IIRNotch:
    def __init__(self, freq: float, sample_rate: float, q: float = 10.0):
        w0 = 2 * math.pi * freq / sample_rate
        alpha = math.sin(w0) / (2 * q)
        b0 = 1.0
        b1 = -2 * math.cos(w0)
        b2 = 1.0
        a0 = 1 + alpha
        a1 = -2 * math.cos(w0)
        a2 = 1 - alpha
        self.b0 = b0 / a0
        self.b1 = b1 / a0
        self.b2 = b2 / a0
        self.a1 = a1 / a0
        self.a2 = a2 / a0
        self.z1 = self.z2 = 0.0

    def process(self, x: float) -> float:
        y = self.b0 * x + self.z1
        self.z1 = self.b1 * x - self.a1 * y + self.z2
        self.z2 = self.b2 * x - self.a2 * y
        return y

    def process_block(self, samples: List[float]) -> List[float]:
        return [self.process(s) for s in samples]

if __name__ == "__main__":
    notch = IIRNotch(1000.0, 8000.0, q=5.0)
    sig = [math.sin(2 * math.pi * 1000 * i / 8000) + 0.5 * math.sin(2 * math.pi * 300 * i / 8000) for i in range(200)]
    out = notch.process_block(sig)
    energy_in = sum(x*x for x in sig)
    energy_out = sum(x*x for x in out)
    assert energy_out < energy_in * 0.7
    print("iir_notch self-test passed")
