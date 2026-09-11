"""Suffix automaton (DAWG) for substring queries."""
from __future__ import annotations
from typing import Dict, List


class State:
    __slots__ = ("next", "link", "len", "first_pos")

    def __init__(self):
        self.next: Dict[str, int] = {}
        self.link: int = -1
        self.len: int = 0
        self.first_pos: int = -1


class SuffixAutomaton:
    def __init__(self, text: str = ""):
        self.states: List[State] = [State()]
        self.last = 0
        for ch in text:
            self.extend(ch)

    def extend(self, ch: str) -> None:
        cur = len(self.states)
        self.states.append(State())
        self.states[cur].len = self.states[self.last].len + 1
        self.states[cur].first_pos = self.states[cur].len - 1
        p = self.last
        while p >= 0 and ch not in self.states[p].next:
            self.states[p].next[ch] = cur
            p = self.states[p].link
        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[ch]
            if self.states[p].len + 1 == self.states[q].len:
                self.states[cur].link = q
            else:
                clone = len(self.states)
                self.states.append(State())
                self.states[clone].len = self.states[p].len + 1
                self.states[clone].next = dict(self.states[q].next)
                self.states[clone].link = self.states[q].link
                self.states[clone].first_pos = self.states[q].first_pos
                while p >= 0 and self.states[p].next.get(ch) == q:
                    self.states[p].next[ch] = clone
                    p = self.states[p].link
                self.states[q].link = self.states[cur].link = clone
        self.last = cur

    def contains(self, pattern: str) -> bool:
        state = 0
        for ch in pattern:
            if ch not in self.states[state].next:
                return False
            state = self.states[state].next[ch]
        return True


if __name__ == "__main__":
    sa = SuffixAutomaton("banana")
    assert sa.contains("ana")
    assert sa.contains("nana")
    assert not sa.contains("apple")
    print("suffix_automaton self-tests passed")
