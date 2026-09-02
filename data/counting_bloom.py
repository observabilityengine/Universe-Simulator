"""
Universe Simulator - Counting Bloom Filter
Original support for limited deletions.
"""

from __future__ import annotations

import hashlib
from typing import List


class CountingBloom:
    def __init__(self, size: int = 1024, hashes: int = 4):
        self.size = size
        self.hashes = hashes
        self.counts = [0] * size

    def _indices(self, item: str) -> List[int]:
        idxs = []
        for i in range(self.hashes):
            h = hashlib.sha256(f"{item}:{i}".encode()).hexdigest()
            idxs.append(int(h, 16) % self.size)
        return idxs

    def add(self, item: str) -> None:
        for i in self._indices(item):
            self.counts[i] += 1

    def remove(self, item: str) -> None:
        for i in self._indices(item):
            if self.counts[i] > 0:
                self.counts[i] -= 1

    def contains(self, item: str) -> bool:
        return all(self.counts[i] > 0 for i in self._indices(item))


if __name__ == "__main__":
    cb = CountingBloom(256, 3)
    cb.add("alpha")
    cb.add("beta")
    assert cb.contains("alpha") and cb.contains("beta")
    cb.remove("alpha")
    assert not cb.contains("alpha")
    print("counting_bloom self-test passed")
