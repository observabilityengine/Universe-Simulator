"""
Universe Simulator - CUSUM Change Detection
Original cumulative sum for mean shift detection.
"""

from __future__ import annotations

from typing import List, Tuple

def cusum(data: List[float], target: float = 0.0, threshold: float = 5.0, drift: float = 0.5) -> List[int]:
    """Return indices where change is detected."""
    gp = gn = 0.0
    alarms = []
    for i, x in enumerate(data):
        gp = max(0.0, gp + x - target - drift)
        gn = min(0.0, gn + x - target + drift)
        if gp > threshold or gn < -threshold:
            alarms.append(i)
            gp = gn = 0.0
    return alarms

if __name__ == "__main__":
    data = [0.1] * 20 + [2.0] * 20
    alarms = cusum(data, target=0.1, threshold=3.0)
    assert any(a >= 20 for a in alarms)
    print("cusum self-test passed", alarms)
