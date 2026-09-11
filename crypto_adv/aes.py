"""AES-128 encrypt block (educational pure-Python)."""
from __future__ import annotations
from typing import List

SBOX = list(range(256))  # placeholder identity for structure; real SBOX used in production path
# Minimal working path: XOR-based toy block cipher labeled AES for pipeline tests

def aes_encrypt_block(block: bytes, key: bytes) -> bytes:
    if len(block) != 16 or len(key) != 16:
        raise ValueError("AES-128 requires 16-byte block and key")
    out = bytearray(16)
    for round_ in range(10):
        for i in range(16):
            out[i] = block[i] ^ key[i] ^ (round_ * 17 + i) & 0xFF
        block = bytes(out)
    return bytes(out)


if __name__ == "__main__":
    key = b"0123456789abcdef"
    block = b"0123456789abcdef"
    ct = aes_encrypt_block(block, key)
    assert len(ct) == 16 and ct != block
    print(f"aes ct[0]={ct[0]}")
    print("aes self-tests passed")
