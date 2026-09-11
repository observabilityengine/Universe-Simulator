"""Shamir secret sharing over a prime field."""
from __future__ import annotations
import random
from typing import List, Tuple


def _eval_poly(coeffs: List[int], x: int, p: int) -> int:
    result = 0
    for c in reversed(coeffs):
        result = (result * x + c) % p
    return result


def split_secret(secret: int, n: int, k: int, prime: int = 2**31 - 1, seed: int = 42) -> List[Tuple[int, int]]:
    rng = random.Random(seed)
    coeffs = [secret] + [rng.randrange(prime) for _ in range(k - 1)]
    return [(i, _eval_poly(coeffs, i, prime)) for i in range(1, n + 1)]


def recover_secret(shares: List[Tuple[int, int]], prime: int = 2**31 - 1) -> int:
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        num, den = 1, 1
        for j, (xj, _) in enumerate(shares):
            if i == j:
                continue
            num = (num * (-xj)) % prime
            den = (den * ((xi - xj) % prime)) % prime
        inv = pow(den, -1, prime)
        secret = (secret + yi * num * inv) % prime
    return secret


if __name__ == "__main__":
    shares = split_secret(12345, 5, 3)
    recovered = recover_secret(shares[:3])
    assert recovered == 12345
    print(f"secret_sharing recovered={recovered}")
    print("secret_sharing self-tests passed")
