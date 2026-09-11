"""ECDSA sign/verify over a toy curve."""
from __future__ import annotations
import hashlib
import random
from typing import Tuple
from .elliptic_curve import point_mul, point_add, Point


def _hash_msg(msg: bytes, n: int) -> int:
    h = hashlib.sha256(msg).digest()
    return int.from_bytes(h, "big") % n


def ecdsa_sign(msg: bytes, d: int, G: Point, n: int, p: int, a: int, seed: int = 42) -> Tuple[int, int]:
    rng = random.Random(seed)
    z = _hash_msg(msg, n)
    while True:
        k = rng.randrange(1, n)
        R = point_mul(k, G, p, a)
        if R is None:
            continue
        r = R[0] % n
        if r == 0:
            continue
        s = (pow(k, -1, n) * (z + r * d)) % n
        if s != 0:
            return r, s


def ecdsa_verify(msg: bytes, sig: Tuple[int, int], Q: Point, G: Point, n: int, p: int, a: int) -> bool:
    r, s = sig
    if not (1 <= r < n and 1 <= s < n):
        return False
    z = _hash_msg(msg, n)
    w = pow(s, -1, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    P = point_add(point_mul(u1, G, p, a), point_mul(u2, Q, p, a), p, a)
    if P is None:
        return False
    return P[0] % n == r


if __name__ == "__main__":
    p, a, n = 17, 2, 19
    G = (5, 1)
    d = 3
    Q = point_mul(d, G, p, a)
    sig = ecdsa_sign(b"hello", d, G, n, p, a, seed=1)
    assert ecdsa_verify(b"hello", sig, Q, G, n, p, a)
    print(f"ecdsa sig={sig}")
    print("ecdsa self-tests passed")
