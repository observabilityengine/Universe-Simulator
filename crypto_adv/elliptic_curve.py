"""Elliptic curve arithmetic over prime field (toy curve)."""
from __future__ import annotations
from typing import Optional, Tuple

Point = Optional[Tuple[int, int]]


def modinv(a: int, p: int) -> int:
    return pow(a, -1, p)


def point_add(P: Point, Q: Point, p: int, a: int) -> Point:
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P != Q:
        m = ((y2 - y1) * modinv((x2 - x1) % p, p)) % p
    else:
        m = ((3 * x1 * x1 + a) * modinv((2 * y1) % p, p)) % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)


def point_mul(k: int, P: Point, p: int, a: int) -> Point:
    result = None
    addend = P
    while k:
        if k & 1:
            result = point_add(result, addend, p, a)
        addend = point_add(addend, addend, p, a)
        k >>= 1
    return result


if __name__ == "__main__":
    p, a, b = 17, 2, 2
    G = (5, 1)
    assert point_mul(1, G, p, a) == G
    P2 = point_mul(2, G, p, a)
    assert P2 is not None
    print(f"elliptic_curve 2G={P2}")
    print("elliptic_curve self-tests passed")
