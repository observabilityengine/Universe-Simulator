"""
Universe Simulator - Splay Tree Map
Original top-down splay for key-value storage.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class SMNode:
    key: Any
    value: Any
    left: Optional["SMNode"] = None
    right: Optional["SMNode"] = None

class SplayMap:
    def __init__(self) -> None:
        self.root: Optional[SMNode] = None

    def _splay(self, key: Any, root: Optional[SMNode]) -> Optional[SMNode]:
        if not root:
            return None
        dummy = SMNode(None, None)
        left = right = dummy
        while True:
            if key < root.key:
                if not root.left:
                    break
                if key < root.left.key:
                    tmp = root.left
                    root.left = tmp.right
                    tmp.right = root
                    root = tmp
                    if not root.left:
                        break
                right.left = root
                right = root
                root = root.left
            elif key > root.key:
                if not root.right:
                    break
                if key > root.right.key:
                    tmp = root.right
                    root.right = tmp.left
                    tmp.left = root
                    root = tmp
                    if not root.right:
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

    def insert(self, key: Any, value: Any) -> None:
        if not self.root:
            self.root = SMNode(key, value)
            return
        self.root = self._splay(key, self.root)
        if self.root.key == key:
            self.root.value = value
            return
        node = SMNode(key, value)
        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node

    def search(self, key: Any) -> Optional[Any]:
        if not self.root:
            return None
        self.root = self._splay(key, self.root)
        if self.root and self.root.key == key:
            return self.root.value
        return None

if __name__ == "__main__":
    m = SplayMap()
    m.insert(5, "a")
    m.insert(3, "b")
    m.insert(7, "c")
    assert m.search(5) == "a" and m.search(3) == "b" and m.search(1) is None
    print("splay_map self-test passed")
