"""Tarjan's strongly connected components.

Complexity: O(V+E). Original implementation.
"""
from __future__ import annotations
from typing import List, Tuple

def tarjan_scc(n: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    index = 0
    stack = []
    onstack = [False]*n
    indices = [-1]*n
    lowlink = [-1]*n
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        onstack[v] = True
        for w in adj[v]:
            if indices[w] < 0:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif onstack[w]:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                onstack[w] = False
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in range(n):
        if indices[v] < 0:
            strongconnect(v)
    return sccs

if __name__ == "__main__":
    edges = [(0,1),(1,2),(2,0),(2,3)]
    sccs = tarjan_scc(4, edges)
    assert len(sccs) == 2
    sizes = sorted(len(s) for s in sccs)
    assert sizes == [1, 3]
    print("tarjan_scc self-tests passed")
