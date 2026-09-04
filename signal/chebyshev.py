"""
Universe Simulator - Chebyshev Type-I Low-Pass (2nd order)
Original bilinear design with ripple parameter.
"""

from __future__ import annotations

import math
from typing import List

class ChebyshevLP:
    def __init__(self, cutoff: float, sample_rate: float, ripple_db: float = 1.0):
        eps = math.sqrt(10 ** (ripple_db / 10) - 1)
        w0 = 2 * math.pi * cutoff / sample_rate
        # simplified coefficients
        g = math.sinh((1/2) * math.asinh(1/eps))
        a0 = 1 + 2*g*math.sin(w0) + g*g
        self.b0 = (1 - math.cos(w0)) / (2 * a0)
        self.b1 = (1 - math.cos(w0)) / a0
        self.b2 = self.b0
        self.a1 = (-2 * math.cos(w0) + 2*g*g) / a0
        self.a2 = (1 - 2*g*math.sin(w0) + g*g) / a0
        self.z1 = self.z2 = 0.0

    def process(self, x: float) -> float:
        y = self.b0 * x + self.z1
        self.z1 = self.b1 * x - self.a1 * y + self.z2
        self.z2 = self.b2 * x - self.a2 * y
        return y

    def process_block(self, samples: List[float]) -> List[float]:
        return [self.process(s) for s in samples]

if __name__ == "__main__":
    filt = ChebyshevLP(400.0, 8000.0)
    high = [math.sin(2 * math.pi * 2000 * i / 8000) for i in range(100)]
    out = filt.process_block(high)
    ratio = sum(x*x for x in out) / (sum(x*x for x in high) + 1e-12)
    assert ratio < 0.5
    print("chebyshev self-test passed", ratio)
