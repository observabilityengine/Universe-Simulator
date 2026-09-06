"""Reservoir sampling (Algorithm R) — uniform sample of k items from a stream.

Complexity: O(n) time, O(k) space for stream of length n.
Each item has equal probability k/n of inclusion.
Original implementation.
"""
from __future__ import annotations

import random
from typing import Iterable, List, TypeVar

T = TypeVar("T")


def reservoir_sample(stream: Iterable[T], k: int, seed: int | None = None) -> List[T]:
    """Return a uniform random sample of size min(k, n) from stream."""
    if k < 0:
        raise ValueError("k must be >= 0")
    rng = random.Random(seed)
    reservoir: List[T] = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = rng.randint(0, i)
            if j < k:
                reservoir[j] = item
    return reservoir


if __name__ == "__main__":
    data = list(range(100))
    s = reservoir_sample(data, 10, seed=42)
    assert len(s) == 10
    assert all(x in data for x in s)
    assert reservoir_sample(data, 0) == []
    assert reservoir_sample([1, 2, 3], 5) == [1, 2, 3]
    assert reservoir_sample([], 3) == []
    # reproducibility
    assert reservoir_sample(data, 5, seed=1) == reservoir_sample(data, 5, seed=1)
    print("reservoir_sampling self-tests passed")
