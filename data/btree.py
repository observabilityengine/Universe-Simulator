"""
Universe Simulator - B-Tree (order 3 demo)
Original minimal B-tree for integer keys.
"""

from __future__ import annotations

from typing import List, Optional


class BNode:
    def __init__(self, leaf: bool = True):
        self.keys: List[int] = []
        self.children: List["BNode"] = []
        self.leaf = leaf


class BTree:
    def __init__(self, t: int = 2):
        self.root = BNode()
        self.t = t  # minimum degree

    def search(self, k: int, node: Optional[BNode] = None) -> bool:
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == k:
            return True
        if node.leaf:
            return False
        return self.search(k, node.children[i])

    def insert(self, k: int) -> None:
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_nonfull(new_root, k)
        else:
            self._insert_nonfull(root, k)

    def _insert_nonfull(self, node: BNode, k: int) -> None:
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], k)

    def _split_child(self, parent: BNode, i: int) -> None:
        t = self.t
        y = parent.children[i]
        z = BNode(leaf=y.leaf)
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:]
        y.keys = y.keys[: t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]


if __name__ == "__main__":
    bt = BTree(t=2)
    for v in [10, 20, 5, 6, 12, 30, 7, 17]:
        bt.insert(v)
    assert bt.search(6) and bt.search(17) and not bt.search(99)
    print("btree self-test passed")
