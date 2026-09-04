"""
Universe Simulator - Hilbert-Huang Transform (simplified EMD)
Original empirical mode decomposition for 1-D signal.
"""

from __future__ import annotations

from typing import List, Tuple

def _find_extrema(data: List[float]) -> Tuple[List[int], List[int]]:
    maxs, mins = [], []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            maxs.append(i)
        if data[i] < data[i-1] and data[i] < data[i+1]:
            mins.append(i)
    return maxs, mins

def _envelope(data: List[float], idxs: List[int]) -> List[float]:
    if len(idxs) < 2:
        return [sum(data)/len(data)] * len(data)
    env = [0.0] * len(data)
    for i in range(len(data)):
        # linear interpolation
        for j in range(len(idxs) - 1):
            if idxs[j] <= i <= idxs[j+1]:
                t = (i - idxs[j]) / (idxs[j+1] - idxs[j])
                env[i] = data[idxs[j]] * (1 - t) + data[idxs[j+1]] * t
                break
        else:
            env[i] = data[idxs[-1]] if i > idxs[-1] else data[idxs[0]]
    return env

def emd(data: List[float], max_imfs: int = 3) -> List[List[float]]:
    imfs = []
    residue = data[:]
    for _ in range(max_imfs):
        h = residue[:]
        for _ in range(5):  # sifting
            maxs, mins = _find_extrema(h)
            if len(maxs) < 2 or len(mins) < 2:
                break
            upper = _envelope(h, maxs)
            lower = _envelope(h, mins)
            mean = [(u + l) / 2 for u, l in zip(upper, lower)]
            h = [x - m for x, m in zip(h, mean)]
        imfs.append(h)
        residue = [r - h_ for r, h_ in zip(residue, h)]
    imfs.append(residue)
    return imfs

if __name__ == "__main__":
    import math
    sig = [math.sin(i * 0.2) + 0.5 * math.sin(i * 0.5) for i in range(64)]
    imfs = emd(sig, max_imfs=2)
    assert len(imfs) >= 2
    print("hilbert_huang self-test passed", len(imfs))
