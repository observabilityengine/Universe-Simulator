"""Knuth-Morris-Pratt string matching.

Complexity: O(n + m). Original implementation.
"""
from __future__ import annotations

from typing import List


def kmp_table(pattern: str) -> List[int]:
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """Return starting indices of all occurrences of pattern in text."""
    if not pattern:
        return list(range(len(text) + 1))
    lps = kmp_table(pattern)
    matches = []
    i = j = 0
    n, m = len(text), len(pattern)
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return matches


if __name__ == "__main__":
    assert kmp_search("ababcabcabababd", "ababd") == [10]
    assert kmp_search("aaaa", "aa") == [0, 1, 2]
    assert kmp_search("hello", "x") == []
    assert kmp_search("abc", "") == [0, 1, 2, 3]
    print("kmp self-tests passed")
