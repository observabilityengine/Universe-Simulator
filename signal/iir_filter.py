"""
Universe Simulator - Simple Biquad IIR Filter (low-pass)
Original Direct Form I implementation.
"""

from __future__ import annotations

import math
from typing import List


class BiquadLowPass:
    def __init__(self, cutoff: float, sample_rate: float, q: float = 0.7071):
        w0 = 2 * math.pi * cutoff / sample_rate
        alpha = math.sin(w0) / (2 * q)
        cosw = math.cos(w0)
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
        self.x1 = self.x2 = self.y1 = self.y2 = 0.0

    def process(self, x: float) -> float:
        y = self.b0 * x + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
        self.x2 = self.x1
        self.x1 = x
        self.y2 = self.y1
        self.y1 = y
        return y

    def process_block(self, samples: List[float]) -> List[float]:
        return [self.process(s) for s in samples]


if __name__ == "__main__":
    filt = BiquadLowPass(cutoff=500.0, sample_rate=8000.0)
    # high-freq signal should be attenuated
    high = [math.sin(2 * math.pi * 2000 * i / 8000) for i in range(128)]
    out = filt.process_block(high)
    energy_in = sum(x*x for x in high)
    energy_out = sum(x*x for x in out)
    assert energy_out < energy_in * 0.5
    print("iir_filter self-test passed", energy_out / energy_in)
