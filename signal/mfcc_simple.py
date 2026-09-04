"""
Universe Simulator - Simplified MFCC
Original mel-filterbank + DCT for feature extraction.
"""

from __future__ import annotations

import math
from typing import List

def _hz_to_mel(hz: float) -> float:
    return 2595 * math.log10(1 + hz / 700)

def _mel_to_hz(mel: float) -> float:
    return 700 * (10 ** (mel / 2595) - 1)

def mfcc(samples: List[float], sample_rate: float = 16000.0, n_mfcc: int = 13, n_filt: int = 20) -> List[float]:
    n = len(samples)
    # power spectrum
    spectrum = []
    for k in range(n // 2):
        re = sum(samples[i] * math.cos(2 * math.pi * k * i / n) for i in range(n))
        im = sum(samples[i] * math.sin(2 * math.pi * k * i / n) for i in range(n))
        spectrum.append(re*re + im*im)
    # mel filterbank
    low_mel = _hz_to_mel(0)
    high_mel = _hz_to_mel(sample_rate / 2)
    mel_points = [low_mel + i * (high_mel - low_mel) / (n_filt + 1) for i in range(n_filt + 2)]
    hz_points = [_mel_to_hz(m) for m in mel_points]
    bins = [int(h * n / sample_rate) for h in hz_points]
    filterbank = []
    for i in range(1, n_filt + 1):
        f = [0.0] * (n // 2)
        for j in range(bins[i-1], bins[i]):
            f[j] = (j - bins[i-1]) / (bins[i] - bins[i-1] + 1e-9)
        for j in range(bins[i], bins[i+1]):
            f[j] = (bins[i+1] - j) / (bins[i+1] - bins[i] + 1e-9)
        filterbank.append(f)
    # log energy
    log_energy = []
    for f in filterbank:
        e = sum(f[k] * spectrum[k] for k in range(len(spectrum))) + 1e-10
        log_energy.append(math.log(e))
    # DCT
    mfccs = []
    for m in range(n_mfcc):
        s = sum(log_energy[k] * math.cos(math.pi * m * (k + 0.5) / n_filt) for k in range(n_filt))
        mfccs.append(s)
    return mfccs

if __name__ == "__main__":
    samples = [math.sin(2 * math.pi * 440 * i / 16000) for i in range(512)]
    feats = mfcc(samples)
    assert len(feats) == 13
    print("mfcc_simple self-test passed", feats[0])
