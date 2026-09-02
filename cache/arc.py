"""
Universe Simulator - Adaptive Replacement Cache (ARC) simplified
Original ARC-like dual-list cache.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Hashable, Optional


class ARC:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity >= 1")
        self.capacity = capacity
        self.p = 0  # target size for T1
        self.t1: OrderedDict = OrderedDict()
        self.t2: OrderedDict = OrderedDict()
        self.b1: OrderedDict = OrderedDict()
        self.b2: OrderedDict = OrderedDict()

    def get(self, key: Hashable) -> Optional[Any]:
        if key in self.t1:
            val = self.t1.pop(key)
            self.t2[key] = val
            return val
        if key in self.t2:
            self.t2.move_to_end(key)
            return self.t2[key]
        return None

    def put(self, key: Hashable, value: Any) -> None:
        if key in self.t1 or key in self.t2:
            if key in self.t1:
                self.t1.pop(key)
            self.t2[key] = value
            return
        if len(self.t1) + len(self.t2) >= self.capacity:
            if self.t1:
                old = next(iter(self.t1))
                self.t1.pop(old)
                self.b1[old] = None
            elif self.t2:
                old = next(iter(self.t2))
                self.t2.pop(old)
                self.b2[old] = None
        self.t1[key] = value

    def __len__(self) -> int:
        return len(self.t1) + len(self.t2)


if __name__ == "__main__":
    c = ARC(3)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") == 1
    c.put("d", 4)
    assert len(c) == 3
    print("arc self-test passed")
