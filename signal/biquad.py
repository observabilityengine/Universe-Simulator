"""
Universe Simulator - Biquad Filter (Direct Form I)
Original peaking EQ / low-shelf coefficients.
"""

from __future__ import annotations

import math
from typing import List

class Biquad:
    def __init__(self, b0: float, b1: float, b2: float, a1: float, a2: float):
        self.b0, self.b1, self.b2 = b0, b1, b2
        self.a1, self.a2 = a1, a2
        self.x1 = self.x2 = self.y1 = self.y2 = 0.0

    @classmethod
    def peaking(cls, freq: float, sample_rate: float, gain_db: float, q: float = 1.0) -> "Biquad":
        A = 10 ** (gain_db / 40)
        w0 = 2 * math.pi * freq / sample_rate
        alpha = math.sin(w0) / (2 * q)
        b0 = 1 + alpha * A
        b1 = -2 * math.cos(w0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * math.cos(w0)
        a2 = 1 - alpha / A
        return cls(b0/a0, b1/a0, b2/a0, a1/a0, a2/a0)

    def process(self, x: float) -> float:
        y = self.b0 * x + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
        self.x2, self.x1 = self.x1, x
        self.y2, self.y1 = self.y1, y
        return y

    def process_block(self, samples: List[float]) -> List[float]:
        return [self.process(s) for s in samples]

if __name__ == "__main__":
    eq = Biquad.peaking(1000.0, 44100.0, 6.0)
    sig = [math.sin(2 * math.pi * 1000 * i / 44100) for i in range(100)]
    out = eq.process_block(sig)
    assert abs(out[50]) > abs(sig[50]) * 1.2
    print("biquad self-test passed")
