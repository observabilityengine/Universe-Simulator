"""Manacher's algorithm for longest palindromic substring."""
from __future__ import annotations
from typing import Tuple


def manacher(s: str) -> Tuple[str, int]:
    """Return (longest_palindrome, center_index_in_original)."""
    if not s:
        return "", 0
    t = "#" + "#".join(s) + "#"
    n = len(t)
    p = [0] * n
    center = right = 0
    for i in range(n):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]
    maxlen = max(p)
    idx = p.index(maxlen)
    start = (idx - maxlen) // 2
    return s[start : start + maxlen], start


if __name__ == "__main__":
    pal, start = manacher("babad")
    assert pal in ("bab", "aba") and len(pal) == 3
    pal2, _ = manacher("cbbd")
    assert pal2 == "bb"
    print(f"manacher {pal}")
    print("manacher self-tests passed")
