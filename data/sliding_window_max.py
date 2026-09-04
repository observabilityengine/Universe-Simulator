"""
Universe Simulator - Sliding Window Maximum
Original deque O(n) algorithm.
"""

from __future__ import annotations

from collections import deque
from typing import List

def sliding_window_max(arr: List[float], k: int) -> List[float]:
    if not arr or k <= 0:
        return []
    dq: deque = deque()
    result = []
    for i, val in enumerate(arr):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and arr[dq[-1]] <= val:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(arr[dq[0]])
    return result

if __name__ == "__main__":
    assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    print("sliding_window_max self-test passed")
