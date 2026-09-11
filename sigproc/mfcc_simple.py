"""Simplified MFCC (mel filterbank + DCT)."""
from __future__ import annotations
import math
from typing import List
from .fft import fft


def _hz_to_mel(hz: float) -> float:
    return 2595 * math.log10(1 + hz / 700)


def _mel_to_hz(mel: float) -> float:
    return 700 * (10 ** (mel / 2595) - 1)


def mfcc(x: List[float], sample_rate: float, n_mfcc: int = 13, n_mels: int = 20) -> List[float]:
    X = fft(x)
    n = len(X)
    power = [abs(X[k]) ** 2 for k in range(n // 2 + 1)]
    # mel filterbank
    fmin, fmax = 0.0, sample_rate / 2
    mels = [_mel_to_hz(m) for m in [
        _hz_to_mel(fmin) + i * (_hz_to_mel(fmax) - _hz_to_mel(fmin)) / (n_mels + 1)
        for i in range(n_mels + 2)
    ]]
    bins = [int(f / sample_rate * n) for f in mels]
    fb = []
    for i in range(1, n_mels + 1):
        left, center, right = bins[i - 1], bins[i], bins[i + 1]
        filt = [0.0] * len(power)
        for k in range(left, center):
            if center != left:
                filt[k] = (k - left) / (center - left)
        for k in range(center, right):
            if right != center:
                filt[k] = (right - k) / (right - center)
        energy = sum(filt[k] * power[k] for k in range(len(power)))
        fb.append(math.log(max(energy, 1e-12)))
    # DCT-II
    mfccs = []
    for m in range(n_mfcc):
        s = sum(fb[k] * math.cos(math.pi * m * (k + 0.5) / n_mels) for k in range(n_mels))
        mfccs.append(s)
    return mfccs


if __name__ == "__main__":
    import math as m
    sr = 16000.0
    x = [m.sin(2 * m.pi * 440 * i / sr) for i in range(512)]
    c = mfcc(x, sr, n_mfcc=5)
    assert len(c) == 5
    print(f"mfcc_simple {c}")
    print("mfcc_simple self-tests passed")
