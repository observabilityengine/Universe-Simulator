"""Multi-pattern Rabin-Karp search."""
from __future__ import annotations
from typing import Dict, List, Tuple


def rabin_karp_multi(text: str, patterns: List[str], base: int = 256, mod: int = 10**9 + 7) -> List[Tuple[int, str]]:
    if not patterns:
        return []
    by_len: Dict[int, List[str]] = {}
    for p in patterns:
        by_len.setdefault(len(p), []).append(p)
    results = []
    for m, pats in by_len.items():
        if m == 0 or m > len(text):
            continue
        h = pow(base, m - 1, mod)
        targets = {}
        for p in pats:
            ph = 0
            for ch in p:
                ph = (base * ph + ord(ch)) % mod
            targets.setdefault(ph, []).append(p)
        t_hash = 0
        for i in range(m):
            t_hash = (base * t_hash + ord(text[i])) % mod
        for i in range(len(text) - m + 1):
            if t_hash in targets:
                window = text[i : i + m]
                for p in targets[t_hash]:
                    if window == p:
                        results.append((i, p))
            if i < len(text) - m:
                t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
                if t_hash < 0:
                    t_hash += mod
    return sorted(results)


if __name__ == "__main__":
    hits = rabin_karp_multi("the cat and the dog", ["cat", "dog", "the"])
    assert any(p == "cat" for _, p in hits)
    assert any(p == "the" for _, p in hits)
    print(f"rabin_karp_multi {hits}")
    print("rabin_karp_multi self-tests passed")
