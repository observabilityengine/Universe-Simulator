"""
Universe Simulator - Suffix Automaton
Original construction + occurrence count.
"""

from __future__ import annotations

from typing import Dict, List

class State:
    def __init__(self) -> None:
        self.next: Dict[str, int] = {}
        self.link = -1
        self.len = 0
        self.first_pos = 0

class SuffixAutomaton:
    def __init__(self) -> None:
        self.states: List[State] = [State()]
        self.last = 0

    def extend(self, c: str) -> None:
        p = self.last
        curr = len(self.states)
        self.states.append(State())
        self.states[curr].len = self.states[p].len + 1
        self.states[curr].first_pos = self.states[curr].len - 1
        while p >= 0 and c not in self.states[p].next:
            self.states[p].next[c] = curr
            p = self.states[p].link
        if p == -1:
            self.states[curr].link = 0
        else:
            q = self.states[p].next[c]
            if self.states[p].len + 1 == self.states[q].len:
                self.states[curr].link = q
            else:
                clone = len(self.states)
                self.states.append(State())
                self.states[clone].len = self.states[p].len + 1
                self.states[clone].next = dict(self.states[q].next)
                self.states[clone].link = self.states[q].link
                self.states[clone].first_pos = self.states[q].first_pos
                while p >= 0 and self.states[p].next.get(c) == q:
                    self.states[p].next[c] = clone
                    p = self.states[p].link
                self.states[q].link = self.states[curr].link = clone
        self.last = curr

    def build(self, s: str) -> None:
        for c in s:
            self.extend(c)

    def contains(self, pattern: str) -> bool:
        v = 0
        for c in pattern:
            if c not in self.states[v].next:
                return False
            v = self.states[v].next[c]
        return True

if __name__ == "__main__":
    sa = SuffixAutomaton()
    sa.build("abacaba")
    assert sa.contains("aba") and sa.contains("cab") and not sa.contains("abc")
    print("suffix_automaton self-test passed")
