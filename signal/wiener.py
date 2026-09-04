"""
Universe Simulator - Wiener Filter (1-D stationary)
Original frequency-domain style approximation via autocorrelation.
"""

from __future__ import annotations

from typing import List

def wiener_filter(signal: List[float], noise_var: float = 0.1) -> List[float]:
    # simple spectral subtraction style
    n = len(signal)
    # estimate signal power as variance of signal
    mean = sum(signal) / n
    var = sum((x - mean) ** 2 for x in signal) / n
    snr = var / (noise_var + 1e-12)
    gain = snr / (snr + 1)
    return [gain * (x - mean) + mean for x in signal]

if __name__ == "__main__":
    clean = [math.sin(i * 0.2) for i in range(50)]
    import math
    noisy = [c + 0.3 * math.sin(i * 3.1) for i, c in enumerate(clean)]
    filtered = wiener_filter(noisy, 0.1)
    assert len(filtered) == 50
    print("wiener self-test passed")
