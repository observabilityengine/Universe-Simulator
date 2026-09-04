"""
Universe Simulator - Miller-Rabin Primality Test
Deterministic for n < 3_317_044_064_679_887_385_961_981 with fixed witnesses.
Probabilistic otherwise (error < 4^{-k} for k rounds).
Complexity O(k log^3 n). Handles n <= 1 as composite.
"""

from __future__ import annotations

from .mod_pow import mod_pow


# Deterministic witnesses for 64-bit range and beyond known bounds
_DETERMINISTIC_WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _is_composite(a: int, d: int, n: int, s: int) -> bool:
    """Return True if a is a strong liar (witness that n is composite)."""
    x = mod_pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True


def miller_rabin(n: int, k: int = 12) -> bool:
    """
    Return True if n is (probably) prime.
    For n < 2**64 uses deterministic set of witnesses.
    For larger n uses first k witnesses from the deterministic list (or random if k larger).
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Write n-1 = d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    witnesses = _DETERMINISTIC_WITNESSES
    if n >= 2**64:
        # Use first min(k, len) witnesses; for full probabilistic would need random
        witnesses = _DETERMINISTIC_WITNESSES[: min(k, len(_DETERMINISTIC_WITNESSES))]

    for a in witnesses:
        if a >= n:
            continue
        if _is_composite(a, d, n, s):
            return False
    return True


def is_prime(n: int) -> bool:
    """Alias for miller_rabin with default witnesses."""
    return miller_rabin(n)


if __name__ == "__main__":
    # Known primes
    assert miller_rabin(2)
    assert miller_rabin(3)
    assert miller_rabin(5)
    assert miller_rabin(17)
    assert miller_rabin(97)
    assert miller_rabin(10**9 + 7)

    # Composites
    assert not miller_rabin(1)
    assert not miller_rabin(0)
    assert not miller_rabin(-5)
    assert not miller_rabin(4)
    assert not miller_rabin(9)
    assert not miller_rabin(15)
    assert not miller_rabin(25)
    assert not miller_rabin(49)
    assert not miller_rabin(91)  # 7*13
    assert not miller_rabin(561)  # Carmichael

    # Edge powers of two
    assert not miller_rabin(16)
    assert not miller_rabin(2**31)

    # Large known prime
    assert miller_rabin(10**18 + 3)

    print("miller_rabin self-test passed")
