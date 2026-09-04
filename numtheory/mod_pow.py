"""
Universe Simulator - Modular Exponentiation
Computes (base ** exp) % mod using binary exponentiation.
Handles negative bases, zero/negative exponents, and mod == 1.
Complexity O(log exp). Assumes mod > 0.
"""

from __future__ import annotations


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Return (base ** exp) % mod.
    For exp < 0 raises ValueError (modular inverse not computed here).
    For mod <= 0 raises ValueError.
    Result always in [0, mod-1].
    """
    if mod <= 0:
        raise ValueError("mod must be positive")
    if exp < 0:
        raise ValueError("negative exponents require modular inverse; not supported")
    if mod == 1:
        return 0
    result = 1
    base = base % mod
    if base < 0:
        base += mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result


if __name__ == "__main__":
    # Classic
    assert mod_pow(2, 10, 1000) == 24
    assert mod_pow(3, 5, 13) == 9  # 243 % 13 = 9

    # Zero exp
    assert mod_pow(5, 0, 7) == 1
    assert mod_pow(0, 0, 5) == 1  # conventional 0**0 == 1 in modular context here

    # Base 0
    assert mod_pow(0, 5, 7) == 0
    assert mod_pow(0, 0, 1) == 0

    # Negative base
    assert mod_pow(-2, 3, 5) == 2  # -8 % 5 == 2
    assert mod_pow(-3, 2, 7) == 2  # 9 % 7 == 2

    # Mod 1
    assert mod_pow(123, 456, 1) == 0

    # Large exp
    assert mod_pow(2, 100, 10**9 + 7) == pow(2, 100, 10**9 + 7)

    # Edge: base multiple of mod
    assert mod_pow(15, 3, 5) == 0

    print("mod_pow self-test passed")
