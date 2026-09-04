"""
Universe Simulator - Butterworth Low-Pass Filter (2nd order)
Original bilinear transform coefficients + Direct Form II.
"""

from __future__ import annotations

import math
from typing import List

class ButterworthLP:
    def __init__(self, cutoff: float, sample_rate: float):
        w0 = 2 * math.pi * cutoff / sample_rate
        cosw = math.cos(w0)
        sinw = math.sin(w0)
        alpha = sinw / math.sqrt(2)
        b0 = (1 - cosw) / 2
        b1 = 1 - cosw
        b2 = (1 - cosw) / 2
        a0 = 1 + alpha
        a1 = -2 * cosw
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
    filt = ButterworthLP(cutoff=300.0, sample_rate=8000.0)
    high = [math.sin(2 * math.pi * 1500 * i / 8000) for i in range(100)]
    out = filt.process_block(high)
    energy_ratio = sum(x*x for x in out) / (sum(x*x for x in high) + 1e-12)
    assert energy_ratio < 0.4
    print("butterworth self-test passed", energy_ratio)
