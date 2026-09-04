"""
Universe Simulator - van Emde Boas Map (small universe)
Original insert / get for integer keys.
"""

from __future__ import annotations

from typing import Any, Optional

class VEBMap:
    def __init__(self, u: int):
        if u < 2 or (u & (u - 1)) != 0:
            raise ValueError("u must be power of 2")
        self.u = u
        self.min_key: Optional[int] = None
        self.min_val: Any = None
        self.max_key: Optional[int] = None
        if u > 2:
            self.summary = VEBMap(int(u ** 0.5))
            self.cluster = [VEBMap(int(u ** 0.5)) for _ in range(int(u ** 0.5))]
        else:
            self.summary = None
            self.cluster = None

    def high(self, x: int) -> int:
        return x // int(self.u ** 0.5)

    def low(self, x: int) -> int:
        return x % int(self.u ** 0.5)

    def insert(self, key: int, value: Any) -> None:
        if self.min_key is None:
            self.min_key = self.max_key = key
            self.min_val = value
            return
        if key < self.min_key:
            key, self.min_key = self.min_key, key
            value, self.min_val = self.min_val, value
        if self.u > 2:
            h, l = self.high(key), self.low(key)
            if self.cluster[h].min_key is None:
                self.summary.insert(h, None)
            self.cluster[h].insert(l, value)
        if key > self.max_key:
            self.max_key = key

    def get(self, key: int) -> Optional[Any]:
        if self.min_key is None:
            return None
        if key == self.min_key:
            return self.min_val
        if self.u == 2:
            return None
        return self.cluster[self.high(key)].get(self.low(key))

if __name__ == "__main__":
    m = VEBMap(16)
    m.insert(3, "a"); m.insert(7, "b"); m.insert(12, "c")
    assert m.get(7) == "b" and m.get(3) == "a" and m.get(5) is None
    print("van_emde_map self-test passed")
