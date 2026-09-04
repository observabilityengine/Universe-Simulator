"""
Universe Simulator - HyperLogLog Cardinality Estimator
Original HLL with 4-bit registers.
"""

from __future__ import annotations

import hashlib
import math
from typing import Any

class HyperLogLog:
    def __init__(self, p: int = 10):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = 0.7213 / (1 + 1.079 / self.m)

    def _hash(self, x: Any) -> int:
        h = hashlib.md5(str(x).encode()).hexdigest()
        return int(h, 16)

    def add(self, x: Any) -> None:
        h = self._hash(x)
        idx = h & (self.m - 1)
        w = h >> self.p
        rho = 1
        while w & 1 == 0 and rho < 64:
            w >>= 1
            rho += 1
        if rho > self.registers[idx]:
            self.registers[idx] = rho

    def estimate(self) -> float:
        raw = self.alpha * self.m * self.m / sum(2 ** (-r) for r in self.registers)
        if raw <= 2.5 * self.m:
            zeros = self.registers.count(0)
            if zeros > 0:
                return self.m * math.log(self.m / zeros)
        return raw

if __name__ == "__main__":
    hll = HyperLogLog(8)
    for i in range(500):
        hll.add(i)
    est = hll.estimate()
    assert 200 < est < 1000
    print("hyperloglog self-test passed", est)
