"""
Universe Simulator - B-Tree Map (order 3)
Original insert and search for key-value store.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

class BTreeNode:
    def __init__(self, leaf: bool = True):
        self.keys: List[int] = []
        self.values: List[object] = []
        self.children: List["BTreeNode"] = []
        self.leaf = leaf

class BTreeMap:
    def __init__(self, t: int = 3):
        self.root = BTreeNode()
        self.t = t

    def search(self, key: int) -> Optional[object]:
        return self._search(self.root, key)

    def _search(self, node: BTreeNode, key: int) -> Optional[object]:
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        if node.leaf:
            return None
        return self._search(node.children[i], key)

    def insert(self, key: int, value: object) -> None:
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self._split(new_root, 0)
            self.root = new_root
        self._insert_nonfull(self.root, key, value)

    def _split(self, parent: BTreeNode, i: int) -> None:
        t = self.t
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)
        mid = t - 1
        z.keys = y.keys[mid+1:]
        z.values = y.values[mid+1:]
        parent.keys.insert(i, y.keys[mid])
        parent.values.insert(i, y.values[mid])
        y.keys = y.keys[:mid]
        y.values = y.values[:mid]
        if not y.leaf:
            z.children = y.children[mid+1:]
            y.children = y.children[:mid+1]
        parent.children.insert(i + 1, z)

    def _insert_nonfull(self, node: BTreeNode, key: int, value: object) -> None:
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
            node.keys[i+1] = key
            node.values[i+1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key, value)

if __name__ == "__main__":
    m = BTreeMap()
    m.insert(10, "a")
    m.insert(20, "b")
    m.insert(5, "c")
    assert m.search(10) == "a" and m.search(5) == "c" and m.search(15) is None
    print("btree_map self-test passed")
