"""Longest palindromic substring via Manacher-style radii (simplified).

Complexity: O(n).
Returns the longest palindromic substring. Original implementation.
"""
from __future__ import annotations


def longest_palindromic_substring(s: str) -> str:
    """Return one longest palindromic substring of s."""
    if not s:
        return ""
    # Transform: ^#a#b#c#$ to handle even/odd uniformly
    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    p = [0] * n
    center = right = 0
    for i in range(1, n - 1):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]
    maxlen = max(p)
    idx = p.index(maxlen)
    start = (idx - maxlen) // 2
    return s[start : start + maxlen]


if __name__ == "__main__":
    assert longest_palindromic_substring("babad") in ("bab", "aba")
    assert longest_palindromic_substring("cbbd") == "bb"
    assert longest_palindromic_substring("a") == "a"
    assert longest_palindromic_substring("") == ""
    assert longest_palindromic_substring("racecar") == "racecar"
    print("manacher_lps self-tests passed")
