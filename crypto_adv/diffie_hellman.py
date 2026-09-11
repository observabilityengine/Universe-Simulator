"""Diffie-Hellman key exchange (educational)."""
from __future__ import annotations
import random
from typing import Tuple


def generate_dh_params(bits: int = 32, seed: int = 42) -> Tuple[int, int]:
    p = 0xFFFFFFFB
    g = 5
    return p, g


def generate_private(p: int, seed: int = 1) -> int:
    rng = random.Random(seed)
    return rng.randrange(2, p - 1)


def public_key(private: int, p: int, g: int) -> int:
    return pow(g, private, p)


def shared_secret(private: int, other_public: int, p: int) -> int:
    return pow(other_public, private, p)


if __name__ == "__main__":
    p, g = generate_dh_params()
    a = generate_private(p, 1)
    b = generate_private(p, 2)
    A = public_key(a, p, g)
    B = public_key(b, p, g)
    assert shared_secret(a, B, p) == shared_secret(b, A, p)
    print("diffie_hellman self-tests passed")
