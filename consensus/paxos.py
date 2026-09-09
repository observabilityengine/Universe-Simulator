"""Single-decree Paxos."""
from __future__ import annotations
from typing import Any, List, Optional, Tuple


class PaxosNode:
    def __init__(self, node_id: int):
        self.id = node_id
        self.min_proposal = 0
        self.accepted_proposal = 0
        self.accepted_value: Any = None
        self.learned: Any = None

    def prepare(self, n: int) -> Optional[Tuple[int, Any]]:
        if n > self.min_proposal:
            self.min_proposal = n
            return (self.accepted_proposal, self.accepted_value)
        return None

    def accept(self, n: int, value: Any) -> bool:
        if n >= self.min_proposal:
            self.min_proposal = n
            self.accepted_proposal = n
            self.accepted_value = value
            return True
        return False


def run_paxos(proposers: list, acceptors: list, value: Any) -> Any:
    n = max(a.min_proposal for a in acceptors) + 1
    promises = []
    for a in acceptors:
        r = a.prepare(n)
        if r is not None:
            promises.append(r)
    if len(promises) <= len(acceptors) // 2:
        return None
    highest = max(promises, key=lambda x: x[0])
    chosen = highest[1] if highest[1] is not None else value
    accepts = sum(1 for a in acceptors if a.accept(n, chosen))
    if accepts > len(acceptors) // 2:
        for a in acceptors:
            a.learned = chosen
        return chosen
    return None


if __name__ == "__main__":
    acceptors = [PaxosNode(i) for i in range(3)]
    result = run_paxos([], acceptors, "hello")
    assert result == "hello"
    print(f"paxos learned={result}")
    print("paxos self-tests passed")
