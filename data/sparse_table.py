"""Sparse table for static range idempotent queries (RMQ).

Complexity: O(n log n) build, O(1) query for min/max/gcd-style ops.
Immutable after build. Original implementation for range minimum.
"""
from __future__ import annotations

from typing import Callable, List, Sequence, TypeVar

T = TypeVar("T")


class SparseTable:
    def __init__(self, data: Sequence[T], op: Callable[[T, T], T] | None = None) -> None:
        if not data:
            raise ValueError("data must be non-empty")
        self.n = len(data)
        self.op = op if op is not None else (lambda a, b: a if a <= b else b)
        self.log = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1
        k = self.log[self.n] + 1
        self.st: List[List[T]] = [[None] * self.n for _ in range(k)]  # type: ignore
        self.st[0] = list(data)
        for j in range(1, k):
            for i in range(self.n - (1 << j) + 1):
                self.st[j][i] = self.op(
                    self.st[j - 1][i],
                    self.st[j - 1][i + (1 << (j - 1))],
                )

    def query(self, left: int, right: int) -> T:
        """Inclusive [left, right] query."""
        if left < 0 or right >= self.n or left > right:
            raise IndexError("invalid range")
        j = self.log[right - left + 1]
        return self.op(self.st[j][left], self.st[j][right - (1 << j) + 1])


if __name__ == "__main__":
    st = SparseTable([2, 4, 1, 6, 3, 5])
    assert st.query(0, 2) == 1
    assert st.query(3, 5) == 3
    assert st.query(0, 5) == 1
    assert st.query(1, 1) == 4
    st_max = SparseTable([2, 4, 1], op=lambda a, b: a if a >= b else b)
    assert st_max.query(0, 2) == 4
    try:
        SparseTable([])
        assert False
    except ValueError:
        pass
    print("sparse_table self-tests passed")
