"""
Universe Simulator - Chinese Remainder Theorem
Solves systems of simultaneous congruences x ≡ a_i (mod m_i)
when moduli are pairwise coprime (or more generally when consistent).
Returns the unique solution modulo product of moduli (when pairwise coprime).
Complexity O(n log M) where M is product of moduli.
"""

from __future__ import annotations

from .extended_gcd import extended_gcd, gcd


def crt(remainders: list[int], moduli: list[int]) -> tuple[int, int]:
    """
    Solve x ≡ remainders[i] (mod moduli[i]) for all i.
    Returns (x, M) where x is the solution in [0, M-1] and M = product of moduli
    when the system is consistent and moduli pairwise coprime.
    Raises ValueError if lengths differ, any modulus <= 0, or system inconsistent.
    """
    if len(remainders) != len(moduli):
        raise ValueError("remainders and moduli must have same length")
    if not remainders:
        return 0, 1
    for m in moduli:
        if m <= 0:
            raise ValueError("all moduli must be positive")

    # Normalize remainders into [0, m_i)
    a = [r % m for r, m in zip(remainders, moduli)]
    m = list(moduli)

    # Successive combination
    x, M = a[0], m[0]
    for i in range(1, len(a)):
        ai, mi = a[i], m[i]
        g, inv, _ = extended_gcd(M, mi)
        if (ai - x) % g != 0:
            raise ValueError("system of congruences is inconsistent")
        # Solve M * t ≡ (ai - x) (mod mi)
        # t ≡ (ai - x) * inv(M/g)  (mod mi/g)
        t = ((ai - x) // g) * (inv % (mi // g)) % (mi // g)
        x = x + M * t
        M = M // g * mi  # lcm
        x %= M
    return x, M


def crt_pairwise_coprime(remainders: list[int], moduli: list[int]) -> int:
    """
    Faster path when moduli are known pairwise coprime.
    Returns unique x in [0, product-1].
    """
    if len(remainders) != len(moduli):
        raise ValueError("lengths must match")
    if not remainders:
        return 0
    for m in moduli:
        if m <= 0:
            raise ValueError("moduli must be positive")
    # Check pairwise coprime (optional but safe)
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                raise ValueError("moduli not pairwise coprime")

    prod = 1
    for m in moduli:
        prod *= m
    x = 0
    for ai, mi in zip(remainders, moduli):
        pi = prod // mi
        inv = extended_gcd(pi, mi)[1] % mi
        x = (x + ai * pi * inv) % prod
    return x


if __name__ == "__main__":
    # Classic pairwise
    x, M = crt([2, 3, 2], [3, 5, 7])
    assert x == 23 and M == 105
    assert 23 % 3 == 2 and 23 % 5 == 3 and 23 % 7 == 2

    # Single
    x, M = crt([5], [7])
    assert x == 5 and M == 7

    # Empty
    x, M = crt([], [])
    assert x == 0 and M == 1

    # Inconsistent non-coprime
    try:
        crt([2, 3], [4, 6])  # gcd=2, (2-3) not divisible by 2
        assert False, "should have raised"
    except ValueError:
        pass

    # Consistent non-coprime
    x, M = crt([2, 4], [4, 6])  # x≡2 mod 4, x≡4 mod 6 → x≡10 mod 12
    assert x == 10 and M == 12
    assert 10 % 4 == 2 and 10 % 6 == 4

    # Pairwise helper
    assert crt_pairwise_coprime([2, 3, 2], [3, 5, 7]) == 23

    # Negative remainder normalized
    x, M = crt([-1, 4], [5, 7])
    assert x % 5 == 4 and x % 7 == 4

    print("crt self-test passed")
