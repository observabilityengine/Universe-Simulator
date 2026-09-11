"""Manacher LPS array (palindrome radii at each center)."""
from __future__ import annotations
from typing import List


def manacher_lps(s: str) -> List[int]:
    """Return radius array on transformed string #s0#s1#..."""
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
    return p


if __name__ == "__main__":
    p = manacher_lps("aba")
    assert max(p) >= 3
    print(f"manacher_lps {p}")
    print("manacher_lps self-tests passed")
