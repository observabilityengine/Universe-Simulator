"""B+ tree (order m) for integer keys → values.

Complexity: O(log_m n) search/insert. Original implementation.
Leaf nodes hold key-value pairs; internal nodes hold separators.
"""
from __future__ import annotations

from typing import Any, List, Optional, Tuple


class _Node:
    def __init__(self, leaf: bool = False):
        self.leaf = leaf
        self.keys: List[int] = []
        self.children: List[_Node] = []  # internal
        self.values: List[Any] = []  # leaf only
        self.next: Optional[_Node] = None  # leaf link


class BPlusTree:
    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError("order must be >= 3")
        self.order = order
        self.root = _Node(leaf=True)
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def search(self, key: int) -> Optional[Any]:
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        for i, k in enumerate(node.keys):
            if k == key:
                return node.values[i]
        return None

    def insert(self, key: int, value: Any) -> None:
        root = self.root
        if len(root.keys) == self.order - 1:
            new_root = _Node(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_nonfull(self.root, key, value)
        self._size += 1

    def _insert_nonfull(self, node: _Node, key: int, value: Any) -> None:
        if node.leaf:
            i = 0
            while i < len(node.keys) and node.keys[i] < key:
                i += 1
            node.keys.insert(i, key)
            node.values.insert(i, value)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            if len(node.children[i].keys) == self.order - 1:
                self._split_child(node, i)
                if key >= node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key, value)

    def _split_child(self, parent: _Node, i: int) -> None:
        order = self.order
        mid = order // 2
        y = parent.children[i]
        z = _Node(leaf=y.leaf)
        if y.leaf:
            # Split leaf: promote first key of right
            z.keys = y.keys[mid:]
            z.values = y.values[mid:]
            y.keys = y.keys[:mid]
            y.values = y.values[:mid]
            z.next = y.next
            y.next = z
            parent.keys.insert(i, z.keys[0])
            parent.children.insert(i + 1, z)
        else:
            z.keys = y.keys[mid + 1 :]
            z.children = y.children[mid + 1 :]
            up = y.keys[mid]
            y.keys = y.keys[:mid]
            y.children = y.children[: mid + 1]
            parent.keys.insert(i, up)
            parent.children.insert(i + 1, z)


if __name__ == "__main__":
    t = BPlusTree(order=4)
    for i in range(20):
        t.insert(i, i * 10)
    assert len(t) == 20
    assert t.search(5) == 50
    assert t.search(19) == 190
    assert t.search(100) is None
    t2 = BPlusTree(order=3)
    t2.insert(1, "a")
    t2.insert(2, "b")
    t2.insert(3, "c")
    assert t2.search(2) == "b"
    print("btree_plus self-tests passed")
