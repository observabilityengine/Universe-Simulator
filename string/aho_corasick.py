"""
Universe Simulator - Aho-Corasick multi-pattern matcher
Original implementation.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Set


class ACNode:
    def __init__(self) -> None:
        self.next: Dict[str, "ACNode"] = {}
        self.fail: "ACNode" | None = None
        self.out: Set[str] = set()


class AhoCorasick:
    def __init__(self, patterns: List[str]):
        self.root = ACNode()
        for p in patterns:
            node = self.root
            for ch in p:
                if ch not in node.next:
                    node.next[ch] = ACNode()
                node = node.next[ch]
            node.out.add(p)
        self._build_fail()

    def _build_fail(self) -> None:
        q: deque[ACNode] = deque()
        for node in self.root.next.values():
            node.fail = self.root
            q.append(node)
        while q:
            r = q.popleft()
            for ch, u in r.next.items():
                q.append(u)
                v = r.fail
                while v is not None and ch not in v.next:
                    v = v.fail
                u.fail = v.next[ch] if v and ch in v.next else self.root
                u.out |= u.fail.out

    def find(self, text: str) -> List[str]:
        found = []
        node = self.root
        for ch in text:
            while node is not None and ch not in node.next:
                node = node.fail
            if node is None:
                node = self.root
                continue
            node = node.next[ch]
            for p in node.out:
                found.append(p)
        return found


if __name__ == "__main__":
    ac = AhoCorasick(["he", "she", "his", "hers"])
    res = ac.find("ushers")
    assert "she" in res and "he" in res and "hers" in res
    print("aho_corasick self-test passed", res)
