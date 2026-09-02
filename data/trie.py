"""
Universe Simulator - Trie (prefix tree)
Original insertion / search / prefix count.
"""

from __future__ import annotations

from typing import Dict, Optional


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end = False
        self.count = 0  # words passing through


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

    def starts_with(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.count


if __name__ == "__main__":
    t = Trie()
    for w in ["apple", "app", "apricot", "banana"]:
        t.insert(w)
    assert t.search("app") and not t.search("appl")
    assert t.starts_with("ap") == 3
    print("trie self-test passed")
