"""
Universe Simulator - Simple Yield Curve Bootstrap (linear interpolation)
Original zero-curve construction from deposit rates.
"""

from __future__ import annotations

from typing import List, Tuple


class YieldCurve:
    def __init__(self, tenors: List[float], rates: List[float]):
        """tenors in years, rates continuous zero rates."""
        if len(tenors) != len(rates) or not tenors:
            raise ValueError("tenors and rates must match and be non-empty")
        pairs = sorted(zip(tenors, rates))
        self.tenors = [p[0] for p in pairs]
        self.rates = [p[1] for p in pairs]

    def zero_rate(self, t: float) -> float:
        if t <= self.tenors[0]:
            return self.rates[0]
        if t >= self.tenors[-1]:
            return self.rates[-1]
        for i in range(1, len(self.tenors)):
            if t <= self.tenors[i]:
                t0, t1 = self.tenors[i-1], self.tenors[i]
                r0, r1 = self.rates[i-1], self.rates[i]
                w = (t - t0) / (t1 - t0)
                return r0 + w * (r1 - r0)
        return self.rates[-1]

    def df(self, t: float) -> float:
        import math
        return math.exp(-self.zero_rate(t) * t)


if __name__ == "__main__":
    yc = YieldCurve([0.25, 0.5, 1.0, 2.0], [0.02, 0.025, 0.03, 0.035])
    assert abs(yc.zero_rate(0.75) - 0.0275) < 1e-9
    assert 0.96 < yc.df(1.0) < 0.98
    print("yield_curve self-test passed", yc.zero_rate(0.75), yc.df(1.0))
