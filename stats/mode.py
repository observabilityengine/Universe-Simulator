"""Mode (most frequent value) for hashable sequences.

Complexity: O(n).
Returns the mode; for ties returns the first-seen max-frequency value.
Original implementation.
"""
from __future__ import annotations

from typing import Dict, Hashable, Sequence, TypeVar

T = TypeVar("T", bound=Hashable)


def mode(data: Sequence[T]) -> T:
    if not data:
        raise ValueError("empty data")
    counts: Dict[T, int] = {}
    order: list[T] = []
    for x in data:
        if x not in counts:
            order.append(x)
            counts[x] = 0
        counts[x] += 1
    best = order[0]
    for x in order:
        if counts[x] > counts[best]:
            best = x
    return best


if __name__ == "__main__":
    assert mode([1, 2, 2, 3, 3, 3, 4]) == 3
    assert mode(["a", "b", "a"]) == "a"
    assert mode([7]) == 7
    try:
        mode([])
        assert False
    except ValueError:
        pass
    print("mode self-tests passed")
