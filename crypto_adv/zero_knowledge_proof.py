"""Schnorr-like identification protocol (ZKP of discrete log)."""
from __future__ import annotations
import hashlib
import random
from typing import Tuple


def schnorr_prove(x: int, g: int, p: int, seed: int = 42) -> Tuple[int, int]:
    rng = random.Random(seed)
    r = rng.randrange(1, p - 1)
    t = pow(g, r, p)
    y = pow(g, x, p)
    c = int(hashlib.sha256(f"{t}{y}".encode()).hexdigest(), 16) % (p - 1)
    s = (r + c * x) % (p - 1)
    return t, s


def schnorr_verify(y: int, t: int, s: int, g: int, p: int) -> bool:
    c = int(hashlib.sha256(f"{t}{y}".encode()).hexdigest(), 16) % (p - 1)
    return pow(g, s, p) == (t * pow(y, c, p)) % p


if __name__ == "__main__":
    p, g, x = 23, 5, 7
    y = pow(g, x, p)
    t, s = schnorr_prove(x, g, p)
    assert schnorr_verify(y, t, s, g, p)
    print("zero_knowledge_proof self-tests passed")
