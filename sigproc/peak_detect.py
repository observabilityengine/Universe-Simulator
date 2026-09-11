"""Simple peak detection with optional threshold and min distance."""
from __future__ import annotations
from typing import List


def find_peaks(x: List[float], height: float = None, distance: int = 1) -> List[int]:
    peaks = []
    n = len(x)
    for i in range(1, n - 1):
        if x[i] >= x[i - 1] and x[i] >= x[i + 1]:
            if height is not None and x[i] < height:
                continue
            if peaks and i - peaks[-1] < distance:
                if x[i] > x[peaks[-1]]:
                    peaks[-1] = i
                continue
            peaks.append(i)
    return peaks


if __name__ == "__main__":
    x = [0, 1, 0, 2, 0, 3, 0]
    peaks = find_peaks(x, height=1.5)
    assert peaks == [3, 5]
    print(f"peak_detect {peaks}")
    print("peak_detect self-tests passed")
