"""
Module 80 – Suffix Array + LCP
Prefix-doubling suffix array construction + Kasai LCP.
Complete implementation.
"""

from __future__ import annotations
from typing import List


def suffix_array(s: str) -> List[int]:
    n = len(s)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n
    k = 1
    while True:
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, curr = sa[i - 1], sa[i]
            left = (rank[prev], rank[prev + k] if prev + k < n else -1)
            right = (rank[curr], rank[curr + k] if curr + k < n else -1)
            tmp[curr] = tmp[prev] + (0 if left == right else 1)
        rank = tmp[:]
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


def lcp_array(s: str, sa: List[int]) -> List[int]:
    n = len(s)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] == 0:
            continue
        j = sa[rank[i] - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[rank[i]] = h
        if h > 0:
            h -= 1
    return lcp


if __name__ == "__main__":
    print("Testing Suffix Array...")
    s = "banana"
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    print(f"  String: {s}")
    print(f"  SA:  {sa}")
    print(f"  LCP: {lcp}")
    for i, p in enumerate(sa):
        print(f"    {p}: {s[p:]}  (LCP={lcp[i]})")
    print("Suffix Array module OK.")
