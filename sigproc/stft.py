"""Short-time Fourier transform."""
from __future__ import annotations
import math
from typing import List, Tuple
from .fft import fft


def stft(
    x: List[float],
    frame_size: int = 64,
    hop: int = 32,
    window: str = "hann",
) -> List[List[complex]]:
    n = len(x)
    frames = []
    for start in range(0, max(1, n - frame_size + 1), hop):
        frame = x[start : start + frame_size]
        if len(frame) < frame_size:
            frame = frame + [0.0] * (frame_size - len(frame))
        if window == "hann":
            frame = [frame[i] * (0.5 - 0.5 * math.cos(2 * math.pi * i / (frame_size - 1))) for i in range(frame_size)]
        frames.append(fft(frame))
    return frames


def stft_magnitude(x: List[float], frame_size: int = 64, hop: int = 32) -> List[List[float]]:
    return [[abs(c) for c in frame] for frame in stft(x, frame_size, hop)]


if __name__ == "__main__":
    x = [math.sin(2 * math.pi * 5 * i / 128) for i in range(128)]
    mag = stft_magnitude(x, 32, 16)
    assert len(mag) > 0
    print(f"stft n_frames={len(mag)}")
    print("stft self-tests passed")
