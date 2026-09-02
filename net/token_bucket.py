"""
Universe Simulator - Token Bucket Rate Limiter
Original implementation.
"""

from __future__ import annotations

import time


class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self.last
        self.last = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


if __name__ == "__main__":
    tb = TokenBucket(rate=10.0, capacity=5.0)
    assert tb.allow() and tb.allow()
    print("token_bucket self-test passed", tb.tokens)
