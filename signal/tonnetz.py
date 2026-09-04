"""
Universe Simulator - Tonnetz Features
Original harmonic network projection from chroma.
"""

from __future__ import annotations

import math
from typing import List
from signal.chroma import chroma

def tonnetz(samples: List[float], sample_rate: float = 22050.0) -> List[float]:
    ch = chroma(samples, sample_rate)
    # Tonnetz coordinates: fifths, minor thirds, major thirds
    # 6-D representation
    features = [0.0] * 6
    for i, c in enumerate(ch):
        angle5 = 2 * math.pi * 7 * i / 12  # fifths
        angle_m3 = 2 * math.pi * 3 * i / 12
        angle_M3 = 2 * math.pi * 4 * i / 12
        features[0] += c * math.sin(angle5)
        features[1] += c * math.cos(angle5)
        features[2] += c * math.sin(angle_m3)
        features[3] += c * math.cos(angle_m3)
        features[4] += c * math.sin(angle_M3)
        features[5] += c * math.cos(angle_M3)
    return features

if __name__ == "__main__":
    samples = [math.sin(2 * math.pi * 440 * i / 22050) for i in range(2048)]
    t = tonnetz(samples)
    assert len(t) == 6
    print("tonnetz self-test passed", t[0])
