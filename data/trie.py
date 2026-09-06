"""Trie (prefix tree) for strings.

Complexity: O(m) insert/search/startswith for string length m.
Supports insert, search, starts_with, and delete.
Original implementation.
"""
from __future__ import annotations

from typing import Dict, Optional


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_end = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def delete(self, word: str) -> bool:
        def _delete(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            ch = word[depth]
            if ch not in node.children:
                return False
            should_remove = _delete(node.children[ch], word, depth + 1)
            if should_remove:
                del node.children[ch]
                return len(node.children) == 0 and not node.is_end
            return False

        return _delete(self.root, word, 0) or True  # True if path existed

    def _walk(self, s: str) -> Optional[TrieNode]:
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node


if __name__ == "__main__":
    t = Trie()
    t.insert("apple")
    t.insert("app")
    assert t.search("apple") and t.search("app")
    assert not t.search("appl")
    assert t.starts_with("app") and not t.starts_with("b")
    t.delete("app")
    assert not t.search("app") and t.search("apple")
    t2 = Trie()
    assert not t2.search("")
    t2.insert("")
    assert t2.search("")
    print("trie self-tests passed")
