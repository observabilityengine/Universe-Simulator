"""
Module 52 – Bit Array
Compact bit vector with set/get/count operations.
Original implementation.
"""

from __future__ import annotations
from typing import Iterator


class BitArray:
    def __init__(self, size: int):
        if size < 0:
            raise ValueError("size must be non-negative")
        self.size = size
        self._bytes = bytearray((size + 7) // 8)

    def set(self, index: int, value: bool = True) -> None:
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")
        byte_idx = index // 8
        bit_idx = index % 8
        if value:
            self._bytes[byte_idx] |= (1 << bit_idx)
        else:
            self._bytes[byte_idx] &= ~(1 << bit_idx)

    def get(self, index: int) -> bool:
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")
        byte_idx = index // 8
        bit_idx = index % 8
        return bool(self._bytes[byte_idx] & (1 << bit_idx))

    def count(self) -> int:
        return sum(bin(b).count("1") for b in self._bytes)

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int) -> bool:
        return self.get(index)

    def __setitem__(self, index: int, value: bool) -> None:
        self.set(index, value)

    def iter_set(self) -> Iterator[int]:
        for i in range(self.size):
            if self.get(i):
                yield i


if __name__ == "__main__":
    print("Testing Bit Array...")
    ba = BitArray(100)
    for i in [2, 5, 7, 11, 99]:
        ba.set(i)
    print(f"  Count: {ba.count()}")
    print(f"  Set bits: {list(ba.iter_set())}")
    print(f"  ba[7]={ba[7]}  ba[8]={ba[8]}")
    print("Bit Array module OK.")
