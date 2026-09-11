"""Bank of Goertzel filters for multiple frequencies."""
from __future__ import annotations
from typing import List, Dict
from .goertzel import goertzel_power


def goertzel_bank(samples: List[float], freqs: List[float], sample_rate: float) -> Dict[float, float]:
    return {f: goertzel_power(samples, f, sample_rate) for f in freqs}


if __name__ == "__main__":
    import math
    sr = 100.0
    samples = [math.sin(2 * math.pi * 10 * i / sr) for i in range(100)]
    bank = goertzel_bank(samples, [5.0, 10.0, 20.0], sr)
    assert bank[10.0] == max(bank.values())
    print(f"goertzel_bank {bank}")
    print("goertzel_bank self-tests passed")
