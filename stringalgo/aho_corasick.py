"""Aho-Corasick multi-pattern string matching."""
from __future__ import annotations
from collections import deque
from typing import Dict, List, Tuple


class AhoCorasick:
    def __init__(self):
        self.goto: List[Dict[str, int]] = [{}]
        self.fail: List[int] = [0]
        self.out: List[List[str]] = [[]]

    def add(self, pattern: str) -> None:
        state = 0
        for ch in pattern:
            if ch not in self.goto[state]:
                self.goto[state][ch] = len(self.goto)
                self.goto.append({})
                self.fail.append(0)
                self.out.append([])
            state = self.goto[state][ch]
        self.out[state].append(pattern)

    def build(self) -> None:
        q: deque = deque()
        for ch, s in self.goto[0].items():
            q.append(s)
            self.fail[s] = 0
        while q:
            r = q.popleft()
            for ch, s in self.goto[r].items():
                q.append(s)
                state = self.fail[r]
                while state and ch not in self.goto[state]:
                    state = self.fail[state]
                self.fail[s] = self.goto[state].get(ch, 0)
                self.out[s] = self.out[s] + self.out[self.fail[s]]

    def search(self, text: str) -> List[Tuple[int, str]]:
        """Return list of (end_index, pattern) matches."""
        matches = []
        state = 0
        for i, ch in enumerate(text):
            while state and ch not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(ch, 0)
            for p in self.out[state]:
                matches.append((i, p))
        return matches


if __name__ == "__main__":
    ac = AhoCorasick()
    for p in ["he", "she", "his", "hers"]:
        ac.add(p)
    ac.build()
    hits = ac.search("ushers")
    patterns = {p for _, p in hits}
    assert "he" in patterns and "she" in patterns and "hers" in patterns
    print(f"aho_corasick hits={hits}")
    print("aho_corasick self-tests passed")
