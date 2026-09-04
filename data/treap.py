"""
Universe Simulator - Treap (randomized BST)
Original insert / split / merge / search.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class TreapNode:
    key: int
    prio: float
    left: Optional["TreapNode"] = None
    right: Optional["TreapNode"] = None

def split(root: Optional[TreapNode], key: int) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
    if root is None:
        return None, None
    if root.key < key:
        l, r = split(root.right, key)
        root.right = l
        return root, r
    else:
        l, r = split(root.left, key)
        root.left = r
        return l, root

def merge(left: Optional[TreapNode], right: Optional[TreapNode]) -> Optional[TreapNode]:
    if left is None:
        return right
    if right is None:
        return left
    if left.prio > right.prio:
        left.right = merge(left.right, right)
        return left
    else:
        right.left = merge(left, right.left)
        return right

class Treap:
    def __init__(self, seed: int = 42) -> None:
        self.root: Optional[TreapNode] = None
        self.rng = random.Random(seed)

    def insert(self, key: int) -> None:
        node = TreapNode(key=key, prio=self.rng.random())
        l, r = split(self.root, key)
        self.root = merge(merge(l, node), r)

    def search(self, key: int) -> bool:
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

if __name__ == "__main__":
    t = Treap()
    for k in [5, 3, 7, 1, 9, 4]:
        t.insert(k)
    assert t.search(4) and t.search(9) and not t.search(2)
    print("treap self-test passed")
