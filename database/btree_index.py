"""Classic B-tree index."""
from __future__ import annotations
from typing import Any, List, Optional

ORDER = 3


class BTreeNode:
    def __init__(self, leaf: bool = True):
        self.leaf = leaf
        self.keys: List[Any] = []
        self.values: List[Any] = []
        self.children: List["BTreeNode"] = []


class BTree:
    def __init__(self, t: int = ORDER):
        self.root = BTreeNode(leaf=True)
        self.t = t

    def search(self, key: Any, node: Optional[BTreeNode] = None) -> Optional[Any]:
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        if node.leaf:
            return None
        return self.search(key, node.children[i])

    def insert(self, key: Any, value: Any) -> None:
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new = BTreeNode(leaf=False)
            new.children.append(self.root)
            self._split_child(new, 0)
            self.root = new
        self._insert_nonfull(self.root, key, value)

    def _insert_nonfull(self, node: BTreeNode, key: Any, value: Any) -> None:
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key, value)

    def _split_child(self, parent: BTreeNode, i: int) -> None:
        t = self.t
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)
        parent.keys.insert(i, y.keys[t - 1])
        parent.values.insert(i, y.values[t - 1])
        parent.children.insert(i + 1, z)
        z.keys = y.keys[t:]
        z.values = y.values[t:]
        y.keys = y.keys[: t - 1]
        y.values = y.values[: t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]


if __name__ == "__main__":
    t = BTree()
    for i in range(15):
        t.insert(i, f"v{i}")
    assert t.search(7) == "v7"
    assert t.search(99) is None
    print("btree_index self-tests passed")
