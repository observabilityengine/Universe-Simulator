"""
Module 73 – Knuth-Morris-Pratt String Search
Linear-time pattern matching with prefix table.
Complete implementation.
"""

from __future__ import annotations
from typing import List


def build_lps(pattern: str) -> List[int]:
    n = len(pattern)
    lps = [0] * n
    length = 0
    i = 1
    while i < n:
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
    if not pattern:
        return list(range(len(text) + 1))
    lps = build_lps(pattern)
    result = []
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                result.append(i - j)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return result


if __name__ == "__main__":
    print("Testing KMP...")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    matches = kmp_search(text, pattern)
    print(f"  Text: {text}")
    print(f"  Pattern: {pattern}")
    print(f"  Matches at: {matches}")
    for m in matches:
        print(f"    {text[m:m+len(pattern)]}")
    print("KMP module OK.")
