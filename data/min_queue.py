"""
Universe Simulator - Min Queue (sliding window minimum structure)
Original two-stack method supporting push / pop / min in amortized O(1).
"""

from __future__ import annotations

from typing import List, Tuple

class MinQueue:
    def __init__(self) -> None:
        self.s1: List[Tuple[float, float]] = []  # (value, current_min)
        self.s2: List[Tuple[float, float]] = []

    def push(self, x: float) -> None:
        m = x if not self.s1 else min(x, self.s1[-1][1])
        self.s1.append((x, m))

    def pop(self) -> float:
        if not self.s2:
            while self.s1:
                x, _ = self.s1.pop()
                m = x if not self.s2 else min(x, self.s2[-1][1])
                self.s2.append((x, m))
        return self.s2.pop()[0]

    def get_min(self) -> float:
        if not self.s1 and not self.s2:
            raise IndexError("empty")
        if not self.s1:
            return self.s2[-1][1]
        if not self.s2:
            return self.s1[-1][1]
        return min(self.s1[-1][1], self.s2[-1][1])

if __name__ == "__main__":
    mq = MinQueue()
    mq.push(3)
    mq.push(1)
    mq.push(4)
    assert mq.get_min() == 1
    mq.pop()
    assert mq.get_min() == 1
    mq.pop()
    assert mq.get_min() == 4
    print("min_queue self-test passed")
