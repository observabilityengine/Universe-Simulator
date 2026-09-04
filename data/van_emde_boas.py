"""
Universe Simulator - van Emde Boas Tree (simplified universe size power of 2)
Original insert / member / successor for small u.
"""

from __future__ import annotations

from typing import Optional

class VEB:
    def __init__(self, u: int):
        if u < 2 or (u & (u - 1)) != 0:
            raise ValueError("u must be power of 2 >= 2")
        self.u = u
        self.min: Optional[int] = None
        self.max: Optional[int] = None
        if u > 2:
            self.summary = VEB(int(u ** 0.5))
            self.cluster = [VEB(int(u ** 0.5)) for _ in range(int(u ** 0.5))]
        else:
            self.summary = None
            self.cluster = None

    def high(self, x: int) -> int:
        return x // int(self.u ** 0.5)

    def low(self, x: int) -> int:
        return x % int(self.u ** 0.5)

    def index(self, high: int, low: int) -> int:
        return high * int(self.u ** 0.5) + low

    def member(self, x: int) -> bool:
        if self.min is None:
            return False
        if x == self.min or x == self.max:
            return True
        if self.u == 2:
            return False
        return self.cluster[self.high(x)].member(self.low(x))

    def insert(self, x: int) -> None:
        if self.min is None:
            self.min = self.max = x
            return
        if x < self.min:
            x, self.min = self.min, x
        if self.u > 2:
            h, l = self.high(x), self.low(x)
            if self.cluster[h].min is None:
                self.summary.insert(h)
            self.cluster[h].insert(l)
        if x > self.max:
            self.max = x

    def successor(self, x: int) -> Optional[int]:
        if self.u == 2:
            if x == 0 and self.max == 1:
                return 1
            return None
        if self.min is not None and x < self.min:
            return self.min
        h, l = self.high(x), self.low(x)
        max_low = self.cluster[h].max
        if max_low is not None and l < max_low:
            return self.index(h, self.cluster[h].successor(l))
        succ_cluster = self.summary.successor(h)
        if succ_cluster is None:
            return None
        return self.index(succ_cluster, self.cluster[succ_cluster].min)

if __name__ == "__main__":
    v = VEB(16)
    for x in [2, 3, 4, 5, 7, 14, 15]:
        v.insert(x)
    assert v.member(7) and not v.member(6)
    assert v.successor(5) == 7
    print("van_emde_boas self-test passed")
