"""First-order allpass filter."""
from __future__ import annotations
from typing import List


class Allpass:
    def __init__(self, coef: float):
        """coef in (-1, 1); positive delays high frequencies more."""
        self.a = coef
        self.z = 0.0

    def process(self, x: float) -> float:
        y = -self.a * x + self.z
        self.z = x + self.a * y
        return y

    def process_block(self, data: List[float]) -> List[float]:
        return [self.process(v) for v in data]


if __name__ == "__main__":
    ap = Allpass(0.5)
    impulse = [1.0] + [0.0] * 10
    out = ap.process_block(impulse)
    # energy preserved approximately
    assert abs(sum(o * o for o in out) - 1.0) < 0.2
    print(f"allpass energy={sum(o*o for o in out):.3f}")
    print("allpass self-tests passed")
