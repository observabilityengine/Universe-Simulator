"""
Universe Simulator - AVL Tree
Original self-balancing BST with insert and search.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class AVLNode:
    key: int
    height: int = 1
    left: Optional["AVLNode"] = None
    right: Optional["AVLNode"] = None

class AVLTree:
    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None

    def _height(self, n: Optional[AVLNode]) -> int:
        return n.height if n else 0

    def _balance(self, n: Optional[AVLNode]) -> int:
        return self._height(n.left) - self._height(n.right) if n else 0

    def _update(self, n: AVLNode) -> None:
        n.height = 1 + max(self._height(n.left), self._height(n.right))

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        t = x.right
        x.right = y
        y.left = t
        self._update(y)
        self._update(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        t = y.left
        y.left = x
        x.right = t
        self._update(x)
        self._update(y)
        return y

    def _insert(self, node: Optional[AVLNode], key: int) -> AVLNode:
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node
        self._update(node)
        bal = self._balance(node)
        if bal > 1 and key < node.left.key:
            return self._rotate_right(node)
        if bal < -1 and key > node.right.key:
            return self._rotate_left(node)
        if bal > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bal < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def search(self, key: int) -> bool:
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

if __name__ == "__main__":
    t = AVLTree()
    for k in [10, 20, 30, 40, 50, 25]:
        t.insert(k)
    assert t.search(25) and t.search(40) and not t.search(15)
    print("avl self-test passed")
