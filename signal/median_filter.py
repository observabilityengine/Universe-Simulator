"""
Universe Simulator - 1-D Median Filter
Original sliding-window median.
"""

from __future__ import annotations

from typing import List

def median_filter(data: List[float], window: int = 3) -> List[float]:
    if window % 2 == 0:
        window += 1
    half = window // 2
    n = len(data)
    out = []
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        window_vals = sorted(data[lo:hi])
        out.append(window_vals[len(window_vals) // 2])
    return out

if __name__ == "__main__":
    data = [1.0, 100.0, 2.0, 3.0, 200.0, 4.0]
    filtered = median_filter(data, 3)
    assert filtered[1] == 2.0 and filtered[4] == 4.0
    print("median_filter self-test passed", filtered)
