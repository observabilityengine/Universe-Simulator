"""RSA key generation, encrypt, decrypt (educational, small primes)."""
from __future__ import annotations
import math
import random
from typing import Tuple


def _is_prime(n: int, k: int = 8) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    rng = random.Random(n)
    for _ in range(k):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _gen_prime(bits: int, rng: random.Random) -> int:
    while True:
        p = rng.getrandbits(bits) | 1
        if _is_prime(p):
            return p


def generate_keypair(bits: int = 32, seed: int = 42) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    rng = random.Random(seed)
    p = _gen_prime(bits // 2, rng)
    q = _gen_prime(bits // 2, rng)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while math.gcd(e, phi) != 1:
        e += 2
    d = pow(e, -1, phi)
    return (e, n), (d, n)


def encrypt(msg: int, public: Tuple[int, int]) -> int:
    e, n = public
    return pow(msg, e, n)


def decrypt(cipher: int, private: Tuple[int, int]) -> int:
    d, n = private
    return pow(cipher, d, n)


if __name__ == "__main__":
    pub, priv = generate_keypair(32, seed=1)
    m = 42
    c = encrypt(m, pub)
    assert decrypt(c, priv) == m
    print(f"rsa n_bits={pub[1].bit_length()}")
    print("rsa self-tests passed")
