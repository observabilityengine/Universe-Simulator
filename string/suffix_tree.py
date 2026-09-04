"""
Universe Simulator - Ukkonen Suffix Tree (simplified construction)
Original online suffix tree for substring search.
"""

from __future__ import annotations

from typing import Dict, Optional

class STNode:
    def __init__(self):
        self.children: Dict[str, "STNode"] = {}
        self.start = -1
        self.end = -1
        self.suffix_link: Optional["STNode"] = None

class SuffixTree:
    def __init__(self, text: str):
        self.text = text + "$"
        self.root = STNode()
        self.root.suffix_link = self.root
        self._build()

    def _build(self) -> None:
        # simplified naive construction for correctness
        n = len(self.text)
        for i in range(n):
            node = self.root
            j = i
            while j < n:
                c = self.text[j]
                if c not in node.children:
                    child = STNode()
                    child.start = j
                    child.end = n - 1
                    node.children[c] = child
                    break
                child = node.children[c]
                k = child.start
                while k <= child.end and j < n and self.text[k] == self.text[j]:
                    k += 1
                    j += 1
                if k <= child.end:
                    # split
                    split = STNode()
                    split.start = child.start
                    split.end = k - 1
                    child.start = k
                    split.children[self.text[k]] = child
                    node.children[self.text[split.start]] = split
                    new_leaf = STNode()
                    new_leaf.start = j
                    new_leaf.end = n - 1
                    if j < n:
                        split.children[self.text[j]] = new_leaf
                    break
                node = child

    def contains(self, pattern: str) -> bool:
        node = self.root
        i = 0
        while i < len(pattern):
            c = pattern[i]
            if c not in node.children:
                return False
            child = node.children[c]
            k = child.start
            while k <= child.end and i < len(pattern):
                if self.text[k] != pattern[i]:
                    return False
                k += 1
                i += 1
            node = child
        return True

if __name__ == "__main__":
    st = SuffixTree("banana")
    assert st.contains("ana") and st.contains("nana") and not st.contains("apple")
    print("suffix_tree self-test passed")
