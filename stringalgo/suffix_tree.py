"""Ukkonen-style suffix tree (simplified explicit construction)."""
from __future__ import annotations
from typing import Dict, List, Optional


class SuffixTreeNode:
    def __init__(self):
        self.children: Dict[str, "SuffixTreeNode"] = {}
        self.start: int = -1
        self.end: int = -1
        self.suffix_index: int = -1


class SuffixTree:
    def __init__(self, text: str):
        self.text = text + "$"
        self.root = SuffixTreeNode()
        for i in range(len(self.text)):
            self._add_suffix(i)

    def _add_suffix(self, i: int) -> None:
        node = self.root
        j = i
        while j < len(self.text):
            ch = self.text[j]
            if ch not in node.children:
                leaf = SuffixTreeNode()
                leaf.start = j
                leaf.end = len(self.text) - 1
                leaf.suffix_index = i
                node.children[ch] = leaf
                return
            child = node.children[ch]
            edge = self.text[child.start : child.end + 1]
            k = 0
            while k < len(edge) and j + k < len(self.text) and edge[k] == self.text[j + k]:
                k += 1
            if k == len(edge):
                node = child
                j += k
                continue
            # split
            split = SuffixTreeNode()
            split.start = child.start
            split.end = child.start + k - 1
            node.children[ch] = split
            child.start = child.start + k
            split.children[self.text[child.start]] = child
            leaf = SuffixTreeNode()
            leaf.start = j + k
            leaf.end = len(self.text) - 1
            leaf.suffix_index = i
            split.children[self.text[leaf.start]] = leaf
            return

    def search(self, pattern: str) -> bool:
        node = self.root
        i = 0
        while i < len(pattern):
            ch = pattern[i]
            if ch not in node.children:
                return False
            child = node.children[ch]
            edge = self.text[child.start : child.end + 1]
            for c in edge:
                if i >= len(pattern):
                    return True
                if pattern[i] != c:
                    return False
                i += 1
            node = child
        return True


if __name__ == "__main__":
    st = SuffixTree("banana")
    assert st.search("ana")
    assert st.search("nana")
    assert not st.search("apple")
    print("suffix_tree self-tests passed")
