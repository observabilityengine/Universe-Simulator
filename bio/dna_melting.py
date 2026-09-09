"""DNA melting temperature estimation (Wallace & nearest-neighbour simplified)."""
from __future__ import annotations
import math


def tm_wallace(seq: str) -> float:
    seq = seq.upper()
    at = seq.count("A") + seq.count("T")
    gc = seq.count("G") + seq.count("C")
    return 2 * at + 4 * gc


def tm_gc(seq: str, Na: float = 0.05) -> float:
    seq = seq.upper()
    n = len(seq)
    if n == 0:
        return 0.0
    gc = (seq.count("G") + seq.count("C")) / n * 100
    return 81.5 + 16.6 * math.log10(Na) + 0.41 * gc - 675 / n


if __name__ == "__main__":
    seq = "ATGCATGCATGC"
    tw = tm_wallace(seq)
    tg = tm_gc(seq)
    assert tw > 0 and tg > 0
    print(f"dna_melting Wallace={tw} GC={tg:.1f}")
    print("dna_melting self-tests passed")
