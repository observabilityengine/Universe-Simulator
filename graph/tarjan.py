"""
Universe Simulator - Tarjan Strongly Connected Components
Original DFS-based SCC algorithm.
"""

from __future__ import annotations

from typing import Dict, List, Set


def tarjan_scc(graph: Dict[int, List[int]]) -> List[List[int]]:
    index = 0
    stack: List[int] = []
    on_stack: Set[int] = set()
    indices: Dict[int, int] = {}
    lowlink: Dict[int, int] = {}
    result: List[List[int]] = []

    def strongconnect(v: int) -> None:
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                component.append(w)
                if w == v:
                    break
            result.append(component)

    for v in graph:
        if v not in indices:
            strongconnect(v)
    return result


if __name__ == "__main__":
    g = {0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [5, 3], 5: []}
    sccs = tarjan_scc(g)
    assert any(set(c) == {0, 1, 2} for c in sccs)
    assert any(set(c) == {3, 4} for c in sccs)
    print("tarjan self-test passed", sccs)
