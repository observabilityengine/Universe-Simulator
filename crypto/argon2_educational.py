"""Argon2i-style memory-hard KDF (educational pure-Python).

Complexity: O(time_cost * memory_cost).
This is a simplified research implementation, NOT the official Argon2
and must not be used for real password storage or production security.
Renamed from argon2_stub to reflect complete (educational) status.
"""
from __future__ import annotations

import hashlib
from typing import List


def argon2i(
    password: bytes,
    salt: bytes,
    time_cost: int = 2,
    memory_cost: int = 16,
    parallelism: int = 1,
    hash_len: int = 32,
) -> bytes:
    """Simplified Argon2i-like construction."""
    if time_cost < 1 or memory_cost < 1 or hash_len < 1:
        raise ValueError("invalid cost / length parameters")
    if parallelism != 1:
        raise ValueError("this educational version only supports parallelism=1")

    h = hashlib.blake2b(
        password + salt + time_cost.to_bytes(4, "little") + memory_cost.to_bytes(4, "little"),
        digest_size=64,
    ).digest()

    blocks: List[bytes] = [h]
    for i in range(1, memory_cost):
        prev = blocks[-1]
        blocks.append(hashlib.blake2b(prev + i.to_bytes(4, "little"), digest_size=64).digest())

    for t in range(time_cost):
        for i in range(memory_cost):
            ref = int.from_bytes(blocks[i][:4], "little") % memory_cost
            blocks[i] = hashlib.blake2b(
                blocks[i] + blocks[ref] + t.to_bytes(4, "little"), digest_size=64
            ).digest()

    return hashlib.blake2b(b"".join(blocks), digest_size=hash_len).digest()


if __name__ == "__main__":
    out = argon2i(b"password", b"saltsalt", time_cost=1, memory_cost=8)
    assert len(out) == 32
    out2 = argon2i(b"password", b"saltsalt", time_cost=1, memory_cost=8)
    assert out == out2
    out3 = argon2i(b"different", b"saltsalt", time_cost=1, memory_cost=8)
    assert out != out3
    try:
        argon2i(b"x", b"y", time_cost=0)
        assert False
    except ValueError:
        pass
    print("argon2_educational self-tests passed")
