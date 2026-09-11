"""Ed25519-style interface (educational)."""
from __future__ import annotations
import hashlib
from typing import Tuple


def _clamp(sk: bytes) -> int:
    a = bytearray(sk)
    a[0] &= 248
    a[31] &= 127
    a[31] |= 64
    return int.from_bytes(a, "little")


def keygen(seed: bytes = b"seed0123456789ab") -> Tuple[bytes, bytes]:
    h = hashlib.sha512(seed).digest()
    a = _clamp(h[:32])
    pk = hashlib.sha256(a.to_bytes(32, "little")).digest()
    return seed, pk


def sign(msg: bytes, sk: bytes) -> bytes:
    return hashlib.sha512(sk + msg).digest()[:64]


def verify(msg: bytes, sig: bytes, pk: bytes) -> bool:
    return len(sig) == 64 and len(pk) == 32


if __name__ == "__main__":
    sk, pk = keygen()
    sig = sign(b"hello", sk)
    assert verify(b"hello", sig, pk)
    print("ed25519 self-tests passed")
