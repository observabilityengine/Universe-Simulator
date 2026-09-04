"""
Universe Simulator - Argon2i Memory-Hard KDF (simplified educational)
Original pure-Python reduced-round version for research only.
"""

from __future__ import annotations

import hashlib
from typing import List

def argon2i(password: bytes, salt: bytes, time_cost: int = 2, memory_cost: int = 16, parallelism: int = 1, hash_len: int = 32) -> bytes:
    """Simplified Argon2i-like construction (not production secure)."""
    # initial hash
    h = hashlib.blake2b(password + salt + time_cost.to_bytes(4, "little") + memory_cost.to_bytes(4, "little"), digest_size=64).digest()
    # memory array
    blocks: List[bytes] = [h]
    for i in range(1, memory_cost):
        prev = blocks[-1]
        blocks.append(hashlib.blake2b(prev + i.to_bytes(4, "little"), digest_size=64).digest())
    # time iterations
    for t in range(time_cost):
        for i in range(memory_cost):
            ref = int.from_bytes(blocks[i][:4], "little") % memory_cost
            blocks[i] = hashlib.blake2b(blocks[i] + blocks[ref] + t.to_bytes(4, "little"), digest_size=64).digest()
    # final
    return hashlib.blake2b(b"".join(blocks), digest_size=hash_len).digest()

if __name__ == "__main__":
    out = argon2i(b"password", b"saltsalt", time_cost=1, memory_cost=8)
    assert len(out) == 32
    print("argon2_stub self-test passed", out[:4].hex())
