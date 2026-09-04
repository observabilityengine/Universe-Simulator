"""
Universe Simulator - Radix Tree (Patricia Trie)
Original compressed trie for string keys.
"""

from __future__ import annotations

from typing import Dict, Optional, Any

class RadixNode:
    def __init__(self):
        self.children: Dict[str, "RadixNode"] = {}
        self.value: Any = None
        self.is_end = False

class RadixTree:
    def __init__(self) -> None:
        self.root = RadixNode()

    def insert(self, key: str, value: Any = True) -> None:
        node = self.root
        i = 0
        while i < len(key):
            matched = False
            for edge, child in list(node.children.items()):
                if key.startswith(edge, i):
                    i += len(edge)
                    node = child
                    matched = True
                    break
                # common prefix
                common = 0
                while common < len(edge) and i + common < len(key) and edge[common] == key[i + common]:
                    common += 1
                if common > 0:
                    # split
                    split = RadixNode()
                    split.children[edge[common:]] = child
                    del node.children[edge]
                    node.children[edge[:common]] = split
                    node = split
                    i += common
                    matched = True
                    break
            if not matched:
                node.children[key[i:]] = RadixNode()
                node = node.children[key[i:]]
                i = len(key)
        node.is_end = True
        node.value = value

    def search(self, key: str) -> Optional[Any]:
        node = self.root
        i = 0
        while i < len(key):
            matched = False
            for edge, child in node.children.items():
                if key.startswith(edge, i):
                    i += len(edge)
                    node = child
                    matched = True
                    break
            if not matched:
                return None
        return node.value if node.is_end else None

if __name__ == "__main__":
    rt = RadixTree()
    rt.insert("hello", 1)
    rt.insert("helium", 2)
    rt.insert("world", 3)
    assert rt.search("hello") == 1 and rt.search("helium") == 2 and rt.search("hel") is None
    print("radix_tree self-test passed")
