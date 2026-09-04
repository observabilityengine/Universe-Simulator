"""
Universe Simulator - Order Statistic Tree
Original size-augmented BST supporting select / rank.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class OSNode:
    key: int
    size: int = 1
    left: Optional["OSNode"] = None
    right: Optional["OSNode"] = None

class OrderStatTree:
    def __init__(self) -> None:
        self.root: Optional[OSNode] = None

    def _size(self, n: Optional[OSNode]) -> int:
        return n.size if n else 0

    def _update(self, n: OSNode) -> None:
        n.size = 1 + self._size(n.left) + self._size(n.right)

    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[OSNode], key: int) -> OSNode:
        if not node:
            return OSNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        self._update(node)
        return node

    def select(self, k: int) -> Optional[int]:
        """Return the k-th smallest key (0-based)."""
        return self._select(self.root, k)

    def _select(self, node: Optional[OSNode], k: int) -> Optional[int]:
        if not node:
            return None
        left_size = self._size(node.left)
        if k == left_size:
            return node.key
        if k < left_size:
            return self._select(node.left, k)
        return self._select(node.right, k - left_size - 1)

    def rank(self, key: int) -> int:
        return self._rank(self.root, key)

    def _rank(self, node: Optional[OSNode], key: int) -> int:
        if not node:
            return 0
        if key < node.key:
            return self._rank(node.left, key)
        if key > node.key:
            return 1 + self._size(node.left) + self._rank(node.right, key)
        return self._size(node.left)

if __name__ == "__main__":
    t = OrderStatTree()
    for k in [5, 3, 7, 1, 9]:
        t.insert(k)
    assert t.select(0) == 1 and t.select(2) == 5 and t.rank(7) == 3
    print("order_stat_tree self-test passed")
