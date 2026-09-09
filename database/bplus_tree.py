"""B+ tree index with insert, search, and range scan."""
from __future__ import annotations
from typing import Any, List, Optional, Tuple

ORDER = 4


class BPlusNode:
    def __init__(self, leaf: bool = False):
        self.leaf = leaf
        self.keys: List[Any] = []
        self.children: List[Any] = []
        self.next: Optional["BPlusNode"] = None


class BPlusTree:
    def __init__(self, order: int = ORDER):
        self.root = BPlusNode(leaf=True)
        self.order = order

    def search(self, key: Any) -> Optional[Any]:
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        for i, k in enumerate(node.keys):
            if k == key:
                return node.children[i]
        return None

    def insert(self, key: Any, value: Any) -> None:
        root = self.root
        if len(root.keys) >= 2 * self.order - 1:
            new_root = BPlusNode(leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_nonfull(self.root, key, value)

    def _insert_nonfull(self, node: BPlusNode, key: Any, value: Any) -> None:
        if node.leaf:
            i = 0
            while i < len(node.keys) and node.keys[i] < key:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                node.children[i] = value
                return
            node.keys.insert(i, key)
            node.children.insert(i, value)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            child = node.children[i]
            if len(child.keys) >= 2 * self.order - 1:
                self._split_child(node, i)
                if key >= node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key, value)

    def _split_child(self, parent: BPlusNode, i: int) -> None:
        order = self.order
        node = parent.children[i]
        new = BPlusNode(leaf=node.leaf)
        mid = order - 1
        new.keys = node.keys[mid + 1 :]
        new.children = node.children[mid + 1 :]
        if node.leaf:
            new.next = node.next
            node.next = new
            parent.keys.insert(i, new.keys[0])
        else:
            parent.keys.insert(i, node.keys[mid])
            node.keys = node.keys[:mid]
            node.children = node.children[: mid + 1]
            parent.children.insert(i + 1, new)
            return
        node.keys = node.keys[: mid + 1]
        node.children = node.children[: mid + 1]
        parent.children.insert(i + 1, new)

    def range_query(self, lo: Any, hi: Any) -> List[Tuple[Any, Any]]:
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and lo >= node.keys[i]:
                i += 1
            node = node.children[i]
        result = []
        while node:
            for k, v in zip(node.keys, node.children):
                if lo <= k <= hi:
                    result.append((k, v))
                if k > hi:
                    return result
            node = node.next
        return result


if __name__ == "__main__":
    t = BPlusTree()
    for i in range(20):
        t.insert(i, i * 10)
    assert t.search(5) == 50
    assert t.search(100) is None
    r = t.range_query(3, 7)
    assert len(r) == 5
    print(f"bplus_tree range={r}")
    print("bplus_tree self-tests passed")
