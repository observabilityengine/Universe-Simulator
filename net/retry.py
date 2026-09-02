"""
Module 46 – Retry with Exponential Backoff
Configurable retry policy with jitter.
Original implementation.
"""

from __future__ import annotations
import time
import random
from typing import Callable, Any, Optional, Type, Tuple


def retry(
    func: Callable,
    max_attempts: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 2.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Any:
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except exceptions as e:
            last_exc = e
            if attempt == max_attempts:
                break
            delay = min(max_delay, base_delay * (exponential_base ** (attempt - 1)))
            if jitter:
                delay = delay * (0.5 + random.random())
            time.sleep(delay)
    raise last_exc


if __name__ == "__main__":
    print("Testing Retry...")
    attempts = {"n": 0}
    def flaky():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ConnectionError(f"fail {attempts['n']}")
        return "success"
    result = retry(flaky, max_attempts=5, base_delay=0.01)
    print(f"  Result: {result} after {attempts['n']} attempts")
    print("Retry module OK.")
