"""
Universe Simulator - Extended Euclidean Algorithm
Computes gcd(a, b) and integers x, y such that a*x + b*y = gcd(a, b).
Handles negatives and zeros correctly. Complexity O(log min(|a|, |b|)).
"""

from __future__ import annotations


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Return (g, x, y) where g = gcd(a, b) >= 0 and a*x + b*y = g.
    For a = b = 0 returns (0, 0, 0).
    """
    a0, b0 = abs(a), abs(b)
    if a0 == 0 and b0 == 0:
        return 0, 0, 0
    old_r, r = a0, b0
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    # Adjust signs so that a*x + b*y = g with original a, b
    g = old_r
    x = old_s if a >= 0 else -old_s
    y = old_t if b >= 0 else -old_t
    # Ensure g is non-negative (already is)
    # Final consistency: if original signs make product negative, flip
    if a * x + b * y != g:
        # Rare edge after sign flips; force
        if a * (-x) + b * (-y) == g:
            x, y = -x, -y
    return g, x, y


def gcd(a: int, b: int) -> int:
    """Non-negative gcd."""
    return extended_gcd(a, b)[0]


if __name__ == "__main__":
    # Happy path
    g, x, y = extended_gcd(240, 46)
    assert g == 2 and 240 * x + 46 * y == 2

    # Zero cases
    assert extended_gcd(0, 0) == (0, 0, 0)
    assert extended_gcd(0, 5) == (5, 0, 1)
    assert extended_gcd(7, 0) == (7, 1, 0)
    assert extended_gcd(-7, 0) == (7, -1, 0)
    assert extended_gcd(0, -5) == (5, 0, -1)

    # Negatives
    g, x, y = extended_gcd(-240, 46)
    assert g == 2 and (-240) * x + 46 * y == 2
    g, x, y = extended_gcd(240, -46)
    assert g == 2 and 240 * x + (-46) * y == 2
    g, x, y = extended_gcd(-240, -46)
    assert g == 2 and (-240) * x + (-46) * y == 2

    # Edge: a == b
    g, x, y = extended_gcd(17, 17)
    assert g == 17 and 17 * x + 17 * y == 17

    # Coprime
    g, x, y = extended_gcd(17, 13)
    assert g == 1 and 17 * x + 13 * y == 1

    # Large-ish
    g, x, y = extended_gcd(123456789, 987654321)
    assert g == 9 and 123456789 * x + 987654321 * y == 9

    print("extended_gcd self-test passed")
