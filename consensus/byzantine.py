"""Simplified Byzantine fault-tolerant broadcast (oral messages, n>=3f+1)."""
from __future__ import annotations
from typing import Any, Dict, List


def majority(values: List[Any]) -> Any:
    counts: Dict[Any, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return max(counts, key=counts.get)


def oral_messages(
    commander_value: Any,
    n: int,
    f: int,
    traitors: set,
) -> List[Any]:
    if f == 0:
        return [commander_value] * (n - 1)
    messages = {}
    for i in range(1, n):
        if 0 in traitors:
            messages[i] = f"attack_{i}"
        else:
            messages[i] = commander_value
    decided = []
    for i in range(1, n):
        if i in traitors:
            continue
        received = [messages[i]]
        for j in range(1, n):
            if j == i:
                continue
            if j in traitors:
                received.append(f"lie_{j}")
            else:
                received.append(messages[j])
        decided.append(majority(received))
    return decided


if __name__ == "__main__":
    result = oral_messages("attack", n=4, f=1, traitors={2})
    assert all(v == "attack" for v in result)
    print(f"byzantine decided={result}")
    print("byzantine self-tests passed")
