"""
Universe Simulator - Splay Tree (simplified)
Original top-down splay for insert / search.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SNode:
    key: int
    left: Optional["SNode"] = None
    right: Optional["SNode"] = None


class SplayTree:
    def __init__(self) -> None:
        self.root: Optional[SNode] = None

    def _splay(self, key: int, root: Optional[SNode]) -> Optional[SNode]:
        if root is None:
            return None
        # simplified zig-zag via rotations
        dummy = SNode(0)
        left = right = dummy
        while True:
            if key < root.key:
                if root.left is None:
                    break
                if key < root.left.key:
                    # rotate right
                    tmp = root.left
                    root.left = tmp.right
                    tmp.right = root
                    root = tmp
                    if root.left is None:
                        break
                right.left = root
                right = root
                root = root.left
            elif key > root.key:
                if root.right is None:
                    break
                if key > root.right.key:
                    tmp = root.right
                    root.right = tmp.left
                    tmp.left = root
                    root = tmp
                    if root.right is None:
                        break
                left.right = root
                left = root
                root = root.right
            else:
                break
        left.right = root.left
        right.left = root.right
        root.left = dummy.right
        root.right = dummy.left
        return root

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = SNode(key)
            return
        self.root = self._splay(key, self.root)
        if self.root.key == key:
            return
        node = SNode(key)
        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node

    def search(self, key: int) -> bool:
        if self.root is None:
            return False
        self.root = self._splay(key, self.root)
        return self.root is not None and self.root.key == key


if __name__ == "__main__":
    st = SplayTree()
    for k in [5, 3, 7, 1, 9]:
        st.insert(k)
    assert st.search(7) and st.search(1)
    assert not st.search(4)
    print("splay self-test passed")
