"""
Universe Simulator - Cartesian Tree Map (implicit key by priority)
Original heap-ordered BST with split/merge.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Optional, Tuple

@dataclass
class CTNode:
    key: Any
    value: Any
    prio: float
    left: Optional["CTNode"] = None
    right: Optional["CTNode"] = None

def split(root: Optional[CTNode], key: Any) -> Tuple[Optional[CTNode], Optional[CTNode]]:
    if not root:
        return None, None
    if root.key < key:
        l, r = split(root.right, key)
        root.right = l
        return root, r
    else:
        l, r = split(root.left, key)
        root.left = r
        return l, root

def merge(left: Optional[CTNode], right: Optional[CTNode]) -> Optional[CTNode]:
    if not left: return right
    if not right: return left
    if left.prio > right.prio:
        left.right = merge(left.right, right)
        return left
    right.left = merge(left, right.left)
    return right

class CartesianMap:
    def __init__(self, seed: int = 42) -> None:
        self.root: Optional[CTNode] = None
        self.rng = random.Random(seed)

    def insert(self, key: Any, value: Any) -> None:
        node = CTNode(key, value, self.rng.random())
        l, r = split(self.root, key)
        self.root = merge(merge(l, node), r)

    def search(self, key: Any) -> Optional[Any]:
        cur = self.root
        while cur:
            if key == cur.key: return cur.value
            cur = cur.left if key < cur.key else cur.right
        return None

if __name__ == "__main__":
    m = CartesianMap()
    m.insert(5, "a"); m.insert(3, "b"); m.insert(7, "c")
    assert m.search(5) == "a" and m.search(3) == "b" and m.search(1) is None
    print("cartesian_map self-test passed")
