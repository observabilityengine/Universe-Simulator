"""
Universe Simulator - Scapegoat Tree
Original weight-balanced BST with rebuilding.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SGNode:
    key: int
    left: Optional["SGNode"] = None
    right: Optional["SGNode"] = None
    size: int = 1

class ScapegoatTree:
    def __init__(self, alpha: float = 0.7) -> None:
        self.root: Optional[SGNode] = None
        self.alpha = alpha
        self.max_size = 0

    def _size(self, n: Optional[SGNode]) -> int:
        return n.size if n else 0

    def _update(self, n: SGNode) -> None:
        n.size = 1 + self._size(n.left) + self._size(n.right)

    def _flatten(self, n: Optional[SGNode], out: List[SGNode]) -> None:
        if not n:
            return
        self._flatten(n.left, out)
        out.append(n)
        self._flatten(n.right, out)

    def _build(self, nodes: List[SGNode], lo: int, hi: int) -> Optional[SGNode]:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        n = nodes[mid]
        n.left = self._build(nodes, lo, mid - 1)
        n.right = self._build(nodes, mid + 1, hi)
        self._update(n)
        return n

    def _rebuild(self, n: SGNode) -> SGNode:
        nodes: List[SGNode] = []
        self._flatten(n, nodes)
        return self._build(nodes, 0, len(nodes) - 1)

    def insert(self, key: int) -> None:
        if not self.root:
            self.root = SGNode(key)
            self.max_size = 1
            return
        path = []
        cur = self.root
        while cur:
            path.append(cur)
            if key < cur.key:
                if not cur.left:
                    cur.left = SGNode(key)
                    break
                cur = cur.left
            elif key > cur.key:
                if not cur.right:
                    cur.right = SGNode(key)
                    break
                cur = cur.right
            else:
                return
        for n in reversed(path):
            self._update(n)
        self.max_size = max(self.max_size, self.root.size)
        # check scapegoat
        for i, n in enumerate(path):
            if self._size(n) > self.alpha * self.max_size:
                # rebuild subtree
                rebuilt = self._rebuild(n)
                if i == 0:
                    self.root = rebuilt
                else:
                    parent = path[i - 1]
                    if parent.left is n:
                        parent.left = rebuilt
                    else:
                        parent.right = rebuilt
                break

    def search(self, key: int) -> bool:
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

if __name__ == "__main__":
    t = ScapegoatTree()
    for k in [5, 3, 7, 1, 9, 4, 6]:
        t.insert(k)
    assert t.search(4) and t.search(9) and not t.search(2)
    print("scapegoat self-test passed")
