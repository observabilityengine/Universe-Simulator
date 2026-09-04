"""
Universe Simulator - Vector Clock
Tracks causal partial order across processes.
merge and happens_before are O(n) in number of processes.
Assumes process ids are hashable and stable.
"""

from __future__ import annotations

from typing import Any, Dict, Hashable


class VectorClock:
    def __init__(self, process_id: Hashable, initial: Dict[Hashable, int] | None = None) -> None:
        self.pid = process_id
        self.clock: Dict[Hashable, int] = dict(initial) if initial else {}
        if self.pid not in self.clock:
            self.clock[self.pid] = 0

    def tick(self) -> None:
        """Local event: increment own counter."""
        self.clock[self.pid] = self.clock.get(self.pid, 0) + 1

    def send(self) -> Dict[Hashable, int]:
        """Prepare timestamp for a message; increments own counter."""
        self.tick()
        return dict(self.clock)

    def receive(self, other: Dict[Hashable, int]) -> None:
        """Merge incoming timestamp and increment own counter."""
        for pid, ts in other.items():
            self.clock[pid] = max(self.clock.get(pid, 0), ts)
        self.tick()

    def merge(self, other: "VectorClock") -> None:
        """Component-wise max without incrementing."""
        for pid, ts in other.clock.items():
            self.clock[pid] = max(self.clock.get(pid, 0), ts)

    def happens_before(self, other: "VectorClock") -> bool:
        """True if self → other (strict causal precedence)."""
        less_or_eq = True
        strictly_less = False
        all_pids = set(self.clock) | set(other.clock)
        for pid in all_pids:
            a = self.clock.get(pid, 0)
            b = other.clock.get(pid, 0)
            if a > b:
                less_or_eq = False
                break
            if a < b:
                strictly_less = True
        return less_or_eq and strictly_less

    def concurrent(self, other: "VectorClock") -> bool:
        return not self.happens_before(other) and not other.happens_before(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VectorClock):
            return NotImplemented
        all_pids = set(self.clock) | set(other.clock)
        return all(self.clock.get(p, 0) == other.clock.get(p, 0) for p in all_pids)

    def copy(self) -> "VectorClock":
        return VectorClock(self.pid, dict(self.clock))


if __name__ == "__main__":
    # Causal chain
    a = VectorClock("A")
    b = VectorClock("B")
    a.tick()
    ts = a.send()
    b.receive(ts)
    assert a.happens_before(b)
    assert not b.happens_before(a)
    assert not a.concurrent(b)

    # Concurrent
    c = VectorClock("C")
    d = VectorClock("D")
    c.tick()
    d.tick()
    assert c.concurrent(d)

    # Merge
    e = VectorClock("E")
    f = VectorClock("F")
    e.tick()
    f.tick()
    e.merge(f)
    assert e.clock.get("F", 0) == 1

    # Empty / identity
    g = VectorClock("G")
    h = VectorClock("G")
    assert g == h
    assert not g.happens_before(h)

    # Multi-process causal
    p1 = VectorClock(1)
    p2 = VectorClock(2)
    p3 = VectorClock(3)
    p1.tick()
    t1 = p1.send()
    p2.receive(t1)
    t2 = p2.send()
    p3.receive(t2)
    assert p1.happens_before(p3)
    assert p2.happens_before(p3)

    print("vector_clock self-test passed")
