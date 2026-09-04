"""
Universe Simulator - BLAKE2s (simplified 32-bit, short messages)
Original pure-Python compression for digests.
"""

from __future__ import annotations

def _rotr32(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def blake2s(data: bytes, outlen: int = 32) -> bytes:
    # simplified single-block for short input
    IV = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
          0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
    h = IV[:]
    h[0] ^= 0x01010000 ^ outlen
    # pad message
    msg = data + b"\x00" * (64 - (len(data) % 64 or 64))
    m = [int.from_bytes(msg[i:i+4], "little") for i in range(0, 64, 4)]
    v = h[:] + IV[:]
    v[12] ^= len(data)
    v[14] ^= 0xFFFFFFFF
    # simplified mixing
    for i in range(8):
        v[i] = (v[i] + v[i+4] + m[i % 16]) & 0xFFFFFFFF
        v[i+8] = _rotr32(v[i+8] ^ v[i], 16)
        v[i+4] = (v[i+4] + v[i+8]) & 0xFFFFFFFF
        v[i] = _rotr32(v[i] ^ v[i+4], 12)
    for i in range(8):
        h[i] ^= v[i] ^ v[i+8]
    return b"".join(x.to_bytes(4, "little") for x in h)[:outlen]

if __name__ == "__main__":
    d = blake2s(b"hello")
    assert len(d) == 32
    print("blake2s self-test passed", d[:4].hex())
