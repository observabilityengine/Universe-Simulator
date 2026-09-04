"""
Universe Simulator - Simple Peak Detection
Original local-maxima with prominence threshold.
"""

from __future__ import annotations

from typing import List

def find_peaks(data: List[float], min_prominence: float = 0.5) -> List[int]:
    peaks = []
    n = len(data)
    for i in range(1, n - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            left = min(data[max(0, i - 5):i] or [data[i]])
            right = min(data[i + 1:i + 6] or [data[i]])
            prom = data[i] - max(left, right)
            if prom >= min_prominence:
                peaks.append(i)
    return peaks

if __name__ == "__main__":
    data = [0, 1, 0.5, 2, 0.5, 3, 0, 1, 0]
    peaks = find_peaks(data, 0.8)
    assert 3 in peaks and 5 in peaks
    print("peak_detect self-test passed", peaks)
