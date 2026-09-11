"""Tonnetz (tonal centroid) features from chroma."""
from __future__ import annotations
import math
from typing import List
from .chroma import chroma_vector


def tonnetz(x: List[float], sample_rate: float) -> List[float]:
    """Return 6-D tonnetz vector."""
    ch = chroma_vector(x, sample_rate, 12)
    # fifths, minor thirds, major thirds planes
    r = []
    for interval, n in [(7, 12), (3, 12), (4, 12)]:
        s = sum(ch[i] * math.sin(2 * math.pi * i * interval / n) for i in range(12))
        c = sum(ch[i] * math.cos(2 * math.pi * i * interval / n) for i in range(12))
        r.extend([c, s])
    return r


if __name__ == "__main__":
    import math as m
    sr = 22050.0
    x = [m.sin(2 * m.pi * 440 * i / sr) for i in range(2048)]
    t = tonnetz(x, sr)
    assert len(t) == 6
    print(f"tonnetz {t}")
    print("tonnetz self-tests passed")
