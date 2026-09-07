"""1D median filter.

Complexity: O(n * w log w). Original implementation.
"""
from __future__ import annotations
from typing import List

def median_filter(signal: List[float], window: int = 3) -> List[float]:
    if window % 2 == 0 or window < 1:
        raise ValueError("window must be odd positive")
    half = window // 2
    n = len(signal)
    out = []
    for i in range(n):
        vals = []
        for j in range(i - half, i + half + 1):
            jj = max(0, min(n - 1, j))
            vals.append(signal[jj])
        vals.sort()
        out.append(vals[half])
    return out

if __name__ == "__main__":
    s = [1.0, 2.0, 100.0, 4.0, 5.0]
    m = median_filter(s, 3)
    assert m[2] == 4.0
    assert m[0] == 1.0
    print("median_filter self-tests passed")
