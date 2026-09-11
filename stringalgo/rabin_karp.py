"""Rabin-Karp rolling-hash string search."""
from __future__ import annotations
from typing import List


def rabin_karp_search(text: str, pattern: str, base: int = 256, mod: int = 10**9 + 7) -> List[int]:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    h = pow(base, m - 1, mod)
    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % mod
        t_hash = (base * t_hash + ord(text[i])) % mod
    matches = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i : i + m] == pattern:
            matches.append(i)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if t_hash < 0:
                t_hash += mod
    return matches


if __name__ == "__main__":
    assert rabin_karp_search("ababcabcabababd", "ababd") == [10]
    assert rabin_karp_search("aaaa", "aa") == [0, 1, 2]
    print("rabin_karp self-tests passed")
