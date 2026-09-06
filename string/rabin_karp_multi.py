"""Multi-pattern Rabin-Karp search.

Complexity: average O(n + m + z) for text length n, total pattern length m, z matches.
Returns dict pattern → list of start indices. Original implementation.
"""
from __future__ import annotations

from typing import Dict, List


def rabin_karp_multi(text: str, patterns: List[str], base: int = 256, mod: int = 10**9 + 7) -> Dict[str, List[int]]:
    """Find all occurrences of each pattern in text."""
    result: Dict[str, List[int]] = {p: [] for p in patterns}
    if not text or not patterns:
        return result
    # group by length
    by_len: Dict[int, List[str]] = {}
    for p in patterns:
        if p:
            by_len.setdefault(len(p), []).append(p)
    for length, pats in by_len.items():
        if length > len(text):
            continue
        pat_hash = {}
        for p in pats:
            h = 0
            for ch in p:
                h = (h * base + ord(ch)) % mod
            pat_hash.setdefault(h, []).append(p)
        # rolling hash of text windows
        h = 0
        power = pow(base, length - 1, mod) if length else 1
        for i in range(length):
            h = (h * base + ord(text[i])) % mod
        window = text[0:length]
        if h in pat_hash:
            for p in pat_hash[h]:
                if window == p:
                    result[p].append(0)
        for i in range(length, len(text)):
            h = (h - ord(text[i - length]) * power) % mod
            h = (h * base + ord(text[i])) % mod
            h %= mod
            window = text[i - length + 1 : i + 1]
            if h in pat_hash:
                for p in pat_hash[h]:
                    if window == p:
                        result[p].append(i - length + 1)
    return result


if __name__ == "__main__":
    r = rabin_karp_multi("abracadabra", ["abra", "cad", "xyz"])
    assert r["abra"] == [0, 7]
    assert r["cad"] == [4]
    assert r["xyz"] == []
    assert rabin_karp_multi("", ["a"])["a"] == []
    print("rabin_karp_multi self-tests passed")
