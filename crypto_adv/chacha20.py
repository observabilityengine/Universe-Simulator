"""ChaCha20 stream cipher (core quarter-round + block function)."""
from __future__ import annotations
from typing import List


def _rotl(v: int, n: int) -> int:
    return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF


def _quarterround(s: List[int], a: int, b: int, c: int, d: int) -> None:
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF
    s[d] = _rotl(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF
    s[b] = _rotl(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF
    s[d] = _rotl(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF
    s[b] = _rotl(s[b] ^ s[c], 7)


def chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
    const = b"expand 32-byte k"
    state = []
    for i in range(0, 16, 4):
        state.append(int.from_bytes(const[i : i + 4], "little"))
    for i in range(0, 32, 4):
        state.append(int.from_bytes(key[i : i + 4], "little"))
    state.append(counter & 0xFFFFFFFF)
    for i in range(0, 12, 4):
        state.append(int.from_bytes(nonce[i : i + 4], "little"))
    working = state[:]
    for _ in range(10):
        _quarterround(working, 0, 4, 8, 12)
        _quarterround(working, 1, 5, 9, 13)
        _quarterround(working, 2, 6, 10, 14)
        _quarterround(working, 3, 7, 11, 15)
        _quarterround(working, 0, 5, 10, 15)
        _quarterround(working, 1, 6, 11, 12)
        _quarterround(working, 2, 7, 12, 13)
        _quarterround(working, 3, 4, 13, 14)
    out = b""
    for i in range(16):
        out += ((working[i] + state[i]) & 0xFFFFFFFF).to_bytes(4, "little")
    return out


def chacha20_encrypt(key: bytes, nonce: bytes, plaintext: bytes) -> bytes:
    out = bytearray()
    counter = 0
    for i in range(0, len(plaintext), 64):
        block = chacha20_block(key, counter, nonce)
        counter += 1
        chunk = plaintext[i : i + 64]
        out.extend(b ^ k for b, k in zip(chunk, block))
    return bytes(out)


if __name__ == "__main__":
    key = b"\x00" * 32
    nonce = b"\x00" * 12
    pt = b"Hello ChaCha20!!"
    ct = chacha20_encrypt(key, nonce, pt)
    assert ct != pt
    pt2 = chacha20_encrypt(key, nonce, ct)
    assert pt2 == pt
    print("chacha20 self-tests passed")
