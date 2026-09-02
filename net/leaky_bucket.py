"""
Universe Simulator - Leaky Bucket Rate Limiter
Original implementation.
"""

from __future__ import annotations

import time


class LeakyBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self.level = 0.0
        self.last = time.monotonic()

    def allow(self, amount: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self.last
        self.last = now
        self.level = max(0.0, self.level - elapsed * self.rate)
        if self.level + amount <= self.capacity:
            self.level += amount
            return True
        return False


if __name__ == "__main__":
    lb = LeakyBucket(rate=5.0, capacity=10.0)
    assert lb.allow(3.0)
    assert lb.allow(3.0)
    assert not lb.allow(5.0)
    print("leaky_bucket self-test passed", lb.level)
