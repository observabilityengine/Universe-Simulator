"""
Universe Simulator - First-Order Allpass Filter
Original phase-shifting filter preserving magnitude.
"""

from __future__ import annotations

from typing import List

class Allpass:
    def __init__(self, coeff: float):
        self.a = coeff
        self.z = 0.0

    def process(self, x: float) -> float:
        y = self.a * x + self.z
        self.z = x - self.a * y
        return y

    def process_block(self, samples: List[float]) -> List[float]:
        return [self.process(s) for s in samples]

if __name__ == "__main__":
    ap = Allpass(0.5)
    sig = [1.0, 0.0, 0.0, 0.0, 0.0]
    out = ap.process_block(sig)
    assert abs(sum(x*x for x in out) - sum(x*x for x in sig)) < 1e-9
    print("allpass self-test passed", out)
