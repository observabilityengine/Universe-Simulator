"""
Universe Simulator - Rope (binary tree for strings)
Original concatenation and substring via weight.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class RopeNode:
    weight: int
    left: Optional["RopeNode"] = None
    right: Optional["RopeNode"] = None
    data: Optional[str] = None

class Rope:
    def __init__(self, s: str = "") -> None:
        self.root = RopeNode(weight=len(s), data=s) if s else None

    def _weight(self, n: Optional[RopeNode]) -> int:
        return n.weight if n else 0

    def concat(self, other: "Rope") -> "Rope":
        if not self.root:
            return other
        if not other.root:
            return self
        new = Rope()
        new.root = RopeNode(weight=self._weight(self.root) + self._weight(other.root),
                            left=self.root, right=other.root)
        return new

    def index(self, i: int) -> str:
        node = self.root
        while node and node.data is None:
            if i < self._weight(node.left):
                node = node.left
            else:
                i -= self._weight(node.left)
                node = node.right
        if node and node.data:
            return node.data[i]
        raise IndexError("index out of range")

    def __str__(self) -> str:
        def collect(n: Optional[RopeNode]) -> str:
            if not n:
                return ""
            if n.data is not None:
                return n.data
            return collect(n.left) + collect(n.right)
        return collect(self.root)

if __name__ == "__main__":
    r1 = Rope("hello")
    r2 = Rope(" world")
    r = r1.concat(r2)
    assert str(r) == "hello world"
    assert r.index(0) == "h" and r.index(6) == "w"
    print("rope self-test passed")
