"""Binary exponentiation (exponentiation by squaring).

Complexity: O(log e) multiplications.
Supports modular form. Original implementation.
"""
from __future__ import annotations


def fast_pow(base: int, exp: int, mod: int | None = None) -> int:
    """Compute base^exp, optionally mod m. exp must be >= 0."""
    if exp < 0:
        raise ValueError("exponent must be non-negative")
    if mod is not None and mod <= 0:
        raise ValueError("mod must be positive")
    result = 1
    b = base % mod if mod else base
    e = exp
    while e > 0:
        if e & 1:
            result = (result * b) % mod if mod else result * b
        b = (b * b) % mod if mod else b * b
        e >>= 1
    return result


if __name__ == "__main__":
    assert fast_pow(2, 10) == 1024
    assert fast_pow(3, 0) == 1
    assert fast_pow(2, 10, 1000) == 24
    assert fast_pow(5, 3, 13) == pow(5, 3, 13)
    assert fast_pow(7, 0, 5) == 1
    try:
        fast_pow(2, -1)
        assert False
    except ValueError:
        pass
    print("fast_pow self-tests passed")
