"""
Universe Simulator - Goertzel Filter Bank
Original multi-frequency detection via Goertzel algorithm.
"""

from __future__ import annotations

import math
from typing import List, Dict

def goertzel_bank(samples: List[float], freqs: List[float], sample_rate: float) -> Dict[float, float]:
    n = len(samples)
    results = {}
    for f in freqs:
        k = int(0.5 + (n * f) / sample_rate)
        w = 2 * math.pi * k / n
        coeff = 2 * math.cos(w)
        s0 = s1 = s2 = 0.0
        for x in samples:
            s0 = x + coeff * s1 - s2
            s2 = s1
            s1 = s0
        power = s1*s1 + s2*s2 - coeff * s1 * s2
        results[f] = power
    return results

if __name__ == "__main__":
    sr = 8000.0
    samples = [math.sin(2 * math.pi * 697 * i / sr) + math.sin(2 * math.pi * 1209 * i / sr) for i in range(205)]
    powers = goertzel_bank(samples, [697, 770, 1209, 1336], sr)
    assert powers[697] > powers[770] and powers[1209] > powers[1336]
    print("goertzel_bank self-test passed", powers)
