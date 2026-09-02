"""
Module 35 – Token Bucket Rate Limiter
Thread-safe token bucket.
Original implementation.
"""

from __future__ import annotations
import time
import threading
from typing import Optional


class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        if rate <= 0 or capacity <= 0:
            raise ValueError("rate and capacity must be positive")
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last = now

    def consume(self, tokens: float = 1.0) -> bool:
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def wait(self, tokens: float = 1.0, timeout: Optional[float] = None) -> bool:
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            if self.consume(tokens):
                return True
            if deadline is not None and time.monotonic() >= deadline:
                return False
            time.sleep(0.001)


if __name__ == "__main__":
    print("Testing Token Bucket...")
    bucket = TokenBucket(rate=10.0, capacity=5.0)
    allowed = sum(1 for _ in range(10) if bucket.consume())
    print(f"  Immediate allows: {allowed}/10 (capacity=5)")
    time.sleep(0.3)
    allowed2 = sum(1 for _ in range(5) if bucket.consume())
    print(f"  After 0.3s allows: {allowed2}/5")
    print("Token Bucket module OK.")
