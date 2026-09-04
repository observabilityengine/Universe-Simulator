"""
Universe Simulator - Flajolet-Martin Distinct Counter
Original bitmap sketch for cardinality estimation.
"""

from __future__ import annotations

import hashlib
from typing import Any

class FMSketch:
    def __init__(self, n_bitmaps: int = 32):
        self.n = n_bitmaps
        self.bitmaps = [0] * n_bitmaps

    def _hash(self, x: Any, i: int) -> int:
        h = hashlib.md5(f"{x}:{i}".encode()).hexdigest()
        return int(h, 16)

    def add(self, x: Any) -> None:
        for i in range(self.n):
            h = self._hash(x, i)
            rho = 0
            while h & 1 == 0 and rho < 32:
                h >>= 1
                rho += 1
            self.bitmaps[i] |= (1 << rho)

    def estimate(self) -> float:
        avg = sum(bin(b).count("0") - 1 for b in self.bitmaps) / self.n  # trailing zeros approx
        # better: position of first zero
        rs = []
        for b in self.bitmaps:
            r = 0
            while b & 1:
                b >>= 1
                r += 1
            rs.append(r)
        avg_r = sum(rs) / self.n
        return self.n * (2 ** avg_r) / 0.77351

if __name__ == "__main__":
    fm = FMSketch()
    for i in range(100):
        fm.add(i)
    est = fm.estimate()
    assert 50 < est < 300
    print("fm_sketch self-test passed", est)
