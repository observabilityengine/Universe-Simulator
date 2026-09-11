"""Biquad IIR filter (Direct Form I)."""
from __future__ import annotations
import math
from typing import List, Tuple


class Biquad:
    def __init__(self, b0: float, b1: float, b2: float, a1: float, a2: float):
        self.b0, self.b1, self.b2 = b0, b1, b2
        self.a1, self.a2 = a1, a2
        self.x1 = self.x2 = self.y1 = self.y2 = 0.0

    def process(self, x: float) -> float:
        y = self.b0 * x + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
        self.x2, self.x1 = self.x1, x
        self.y2, self.y1 = self.y1, y
        return y

    def process_block(self, data: List[float]) -> List[float]:
        return [self.process(x) for x in data]


def lowpass_coeffs(fc: float, fs: float, q: float = 0.7071) -> Tuple[float, float, float, float, float]:
    w0 = 2 * math.pi * fc / fs
    alpha = math.sin(w0) / (2 * q)
    cosw = math.cos(w0)
    b0 = (1 - cosw) / 2
    b1 = 1 - cosw
    b2 = (1 - cosw) / 2
    a0 = 1 + alpha
    a1 = -2 * cosw
    a2 = 1 - alpha
    return b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0


if __name__ == "__main__":
    b0, b1, b2, a1, a2 = lowpass_coeffs(10.0, 100.0)
    filt = Biquad(b0, b1, b2, a1, a2)
    impulse = [1.0] + [0.0] * 20
    out = filt.process_block(impulse)
    assert abs(sum(out) - 1.0) < 0.5  # DC gain ~1 for lowpass
    print(f"biquad sum={sum(out):.3f}")
    print("biquad self-tests passed")
