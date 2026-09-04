"""
Universe Simulator - Short-Time Fourier Transform
Original sliding-window DFT spectrogram.
"""

from __future__ import annotations

import math
from typing import List, Tuple

def stft(samples: List[float], window_size: int = 64, hop: int = 32) -> List[List[complex]]:
    n = len(samples)
    frames = []
    for start in range(0, n - window_size + 1, hop):
        frame = samples[start:start + window_size]
        # Hann window
        windowed = [frame[i] * 0.5 * (1 - math.cos(2 * math.pi * i / (window_size - 1))) for i in range(window_size)]
        spectrum = []
        for k in range(window_size // 2 + 1):
            re = sum(windowed[i] * math.cos(2 * math.pi * k * i / window_size) for i in range(window_size))
            im = sum(windowed[i] * math.sin(2 * math.pi * k * i / window_size) for i in range(window_size))
            spectrum.append(complex(re, -im))
        frames.append(spectrum)
    return frames

if __name__ == "__main__":
    samples = [math.sin(2 * math.pi * 5 * i / 64) for i in range(128)]
    spec = stft(samples, 64, 32)
    assert len(spec) > 0 and len(spec[0]) == 33
    print("stft self-test passed", len(spec))
