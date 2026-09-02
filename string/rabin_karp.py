"""
Module 91 – Rabin-Karp String Search
Rolling hash pattern matching.
Complete implementation.
"""

from __future__ import annotations
from typing import List


def rabin_karp(text: str, pattern: str, base: int = 256, mod: int = 10**9 + 7) -> List[int]:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    matches = []
    h = 1
    for _ in range(m - 1):
        h = (h * base) % mod
    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % mod
        t_hash = (base * t_hash + ord(text[i])) % mod
    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i : i + m] == pattern:
                matches.append(i)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if t_hash < 0:
                t_hash += mod
    return matches


if __name__ == "__main__":
    print("Testing Rabin-Karp...")
    text = "GEEKS FOR GEEKS"
    pattern = "GEEK"
    matches = rabin_karp(text, pattern)
    print(f"  Text: {text}")
    print(f"  Pattern: {pattern}")
    print(f"  Matches at: {matches}")
    print("Rabin-Karp module OK.")
