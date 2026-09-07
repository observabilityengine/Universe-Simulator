"""Trie (prefix tree) for string dictionary.

Complexity: O(L) per operation for length L. Original implementation.
"""
from __future__ import annotations

from typing import Dict


class TrieNode:
    __slots__ = ("children", "is_end", "count")

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end = False
        self.count = 0


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True

    def count_prefix(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.count


if __name__ == "__main__":
    t = Trie()
    for w in ["apple", "app", "application", "banana", "band"]:
        t.insert(w)
    assert t.search("app")
    assert t.search("apple")
    assert not t.search("appl")
    assert t.starts_with("ban")
    assert t.count_prefix("app") == 3
    assert t.count_prefix("ban") == 2
    print("trie self-tests passed")
