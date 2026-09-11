"""1-D median filter."""
from __future__ import annotations
from typing import List


def median_filter(data: List[float], window: int = 3) -> List[float]:
    if window < 1 or window % 2 == 0:
        raise ValueError("window must be odd positive integer")
    half = window // 2
    n = len(data)
    out = []
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        w = sorted(data[lo:hi])
        out.append(w[len(w) // 2])
    return out


if __name__ == "__main__":
    data = [1.0, 100.0, 2.0, 3.0, 4.0]
    out = median_filter(data, 3)
    assert out[1] < 50  # spike suppressed
    print(f"median_filter {out}")
    print("median_filter self-tests passed")
