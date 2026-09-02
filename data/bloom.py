"""
Module 34 – Bloom Filter
Probabilistic set membership with tunable false-positive rate.
Original implementation.
"""

from __future__ import annotations
import hashlib
import math
from typing import Any, List


class BloomFilter:
    def __init__(self, capacity: int, error_rate: float = 0.01):
        if capacity < 1 or not (0 < error_rate < 1):
            raise ValueError("Invalid capacity or error_rate")
        self.capacity = capacity
        self.error_rate = error_rate
        self.size = int(-capacity * math.log(error_rate) / (math.log(2) ** 2))
        self.hash_count = max(1, int(self.size / capacity * math.log(2)))
        self.bits = bytearray(self.size)

    def _hashes(self, item: Any) -> List[int]:
        data = str(item).encode()
        h1 = int(hashlib.sha256(data).hexdigest(), 16)
        h2 = int(hashlib.md5(data).hexdigest(), 16)
        return [(h1 + i * h2) % self.size for i in range(self.hash_count)]

    def add(self, item: Any) -> None:
        for pos in self._hashes(item):
            self.bits[pos] = 1

    def __contains__(self, item: Any) -> bool:
        return all(self.bits[pos] for pos in self._hashes(item))

    def fill_ratio(self) -> float:
        return sum(self.bits) / self.size


if __name__ == "__main__":
    print("Testing Bloom Filter...")
    bf = BloomFilter(capacity=1000, error_rate=0.01)
    for i in range(200):
        bf.add(f"item-{i}")
    hits = sum(1 for i in range(200) if f"item-{i}" in bf)
    false_pos = sum(1 for i in range(200, 400) if f"item-{i}" in bf)
    print(f"  True positives: {hits}/200")
    print(f"  False positives: {false_pos}/200")
    print(f"  Fill ratio: {bf.fill_ratio():.3f}")
    print("Bloom Filter module OK.")
