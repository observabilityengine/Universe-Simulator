"""
Universe Simulator - Pure-Python MD5
Original implementation of the MD5 compression (research only).
"""

from __future__ import annotations

import struct
from typing import List


def _left_rotate(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def md5(message: bytes) -> bytes:
    # Constants
    s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4
    K = [int(abs(__import__("math").sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

    a0, b0, c0, d0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

    ml = len(message) * 8
    message += b"\x80"
    message += b"\x00" * ((56 - (len(message) % 64)) % 64)
    message += struct.pack("<Q", ml)

    for i in range(0, len(message), 64):
        M = list(struct.unpack("<16I", message[i:i+64]))
        A, B, C, D = a0, b0, c0, d0
        for j in range(64):
            if j < 16:
                F = (B & C) | ((~B) & D)
                g = j
            elif j < 32:
                F = (D & B) | ((~D) & C)
                g = (5*j + 1) % 16
            elif j < 48:
                F = B ^ C ^ D
                g = (3*j + 5) % 16
            else:
                F = C ^ (B | (~D))
                g = (7*j) % 16
            F = (F + A + K[j] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + _left_rotate(F, s[j])) & 0xFFFFFFFF
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF
    return struct.pack("<4I", a0, b0, c0, d0)


def md5_hex(data: bytes) -> str:
    return md5(data).hex()


if __name__ == "__main__":
    assert md5_hex(b"") == "d41d8cd98f00b204e9800998ecf8427e"
    assert md5_hex(b"abc") == "900150983cd24fb0d6963f7d28e17f72"
    print("pure_md5 self-test passed")
