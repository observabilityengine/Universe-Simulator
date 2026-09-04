"""
Universe Simulator - scrypt KDF (simplified educational)
Original pure-Python reduced version for research only.
"""

from __future__ import annotations

import hashlib
from typing import List

def scrypt(password: bytes, salt: bytes, n: int = 16, r: int = 1, p: int = 1, dklen: int = 32) -> bytes:
    """Simplified scrypt (not production secure)."""
    def salsa20_8(b: bytearray) -> None:
        # minimal mixing
        for _ in range(4):
            for i in range(0, 16, 4):
                b[i] ^= (b[(i+4)%16] + b[(i+8)%16]) & 0xFF

    block = hashlib.pbkdf2_hmac("sha256", password, salt, 1, 128 * r * p)
    # ROMix simplified
    v: List[bytes] = []
    x = block
    for _ in range(n):
        v.append(x)
        x = hashlib.sha256(x).digest()
    for _ in range(n):
        j = int.from_bytes(x[:4], "little") % n
        x = hashlib.sha256(bytes(a ^ b for a, b in zip(x, v[j]))).digest()
    return hashlib.pbkdf2_hmac("sha256", password, x, 1, dklen)

if __name__ == "__main__":
    out = scrypt(b"password", b"salt", n=8)
    assert len(out) == 32
    print("scrypt_stub self-test passed", out[:4].hex())
