"""Chroma (pitch-class) features from magnitude spectrum."""
from __future__ import annotations
import math
from typing import List
from .fft import fft


def chroma_vector(x: List[float], sample_rate: float, n_chroma: int = 12) -> List[float]:
    X = fft(x)
    n = len(X)
    chroma = [0.0] * n_chroma
    for k in range(1, n // 2):
        freq = k * sample_rate / n
        if freq < 20:
            continue
        # MIDI-like pitch class
        midi = 69 + 12 * math.log2(freq / 440.0)
        pc = int(round(midi)) % n_chroma
        chroma[pc] += abs(X[k])
    s = sum(chroma) or 1.0
    return [c / s for c in chroma]


if __name__ == "__main__":
    sr = 22050.0
    # A4 = 440 Hz
    x = [math.sin(2 * math.pi * 440 * i / sr) for i in range(2048)]
    ch = chroma_vector(x, sr)
    assert abs(sum(ch) - 1.0) < 1e-6
    assert ch[9] == max(ch)  # A is pitch class 9
    print(f"chroma peak_pc={ch.index(max(ch))}")
    print("chroma self-tests passed")
