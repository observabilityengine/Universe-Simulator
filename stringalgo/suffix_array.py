"""Suffix array construction (doubling / prefix-doubling)."""
from __future__ import annotations
from typing import List


def suffix_array(s: str) -> List[int]:
    """Return sorted starting indices of suffixes."""
    n = len(s)
    if n == 0:
        return []
    # Sa-is simplified: sort by successive doubling
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n
    k = 1
    while k < n:
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, cur = sa[i - 1], sa[i]
            prev_key = (rank[prev], rank[prev + k] if prev + k < n else -1)
            cur_key = (rank[cur], rank[cur + k] if cur + k < n else -1)
            tmp[cur] = tmp[prev] if prev_key == cur_key else tmp[prev] + 1
        rank, tmp = tmp, rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


def lcp_array(s: str, sa: List[int]) -> List[int]:
    """Kasai LCP array."""
    n = len(s)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp = [0] * n
    h = 0
    for i in range(n):
        r = rank[i]
        if r == 0:
            continue
        j = sa[r - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[r] = h
        if h:
            h -= 1
    return lcp


if __name__ == "__main__":
    s = "banana"
    sa = suffix_array(s)
    assert [s[i:] for i in sa] == sorted(s[i:] for i in range(len(s)))
    lcp = lcp_array(s, sa)
    print(f"suffix_array sa={sa} lcp={lcp}")
    print("suffix_array self-tests passed")
