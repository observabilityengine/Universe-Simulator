"""
Module 42 – Circuit Breaker
Fault-tolerance pattern with closed / open / half-open states.
Original implementation.
"""

from __future__ import annotations
import time
from typing import Callable, Any
from enum import Enum


class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 5.0, half_open_success: int = 2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_success = half_open_success
        self.state = State.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = State.HALF_OPEN
                self.success_count = 0
            else:
                raise RuntimeError("Circuit is OPEN")
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self) -> None:
        if self.state == State.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_success:
                self.state = State.CLOSED
                self.failure_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = State.OPEN
        if self.state == State.HALF_OPEN:
            self.state = State.OPEN


if __name__ == "__main__":
    print("Testing Circuit Breaker...")
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=0.15)
    fail_count = {"n": 0}
    def flaky():
        fail_count["n"] += 1
        if fail_count["n"] <= 3:
            raise ValueError("fail")
        return "ok"
    for i in range(4):
        try:
            r = cb.call(flaky)
            print(i, r, cb.state.value)
        except Exception as e:
            print(i, type(e).__name__, cb.state.value)
    time.sleep(0.2)
    print("after", cb.call(flaky), cb.state.value)
    print("Circuit Breaker module OK.")
