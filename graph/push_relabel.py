"""Push-relabel maximum flow (FIFO variant with gap heuristic omitted for purity).

Complexity: O(V^2 E). Original implementation.
"""
from __future__ import annotations
from collections import deque
from typing import List, Dict, Tuple


def max_flow_push_relabel(n: int, edges: List[Tuple[int, int, int]], source: int, sink: int) -> int:
    """edges = list of (u, v, capacity). Returns max flow value."""
    # Residual graph as adjacency list of [to, cap, rev_index]
    graph: List[List[List[int]]] = [[] for _ in range(n)]
    for u, v, c in edges:
        graph[u].append([v, c, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1])

    height = [0] * n
    excess = [0] * n
    height[source] = n
    # Preflow
    for e in graph[source]:
        v, c, rev = e
        if c > 0:
            e[1] = 0
            graph[v][rev][1] += c
            excess[v] += c
            excess[source] -= c

    active = deque(i for i in range(n) if i != source and i != sink and excess[i] > 0)

    def push(u: int, e: List[int]) -> None:
        v, c, rev = e
        send = min(excess[u], c)
        e[1] -= send
        graph[v][rev][1] += send
        excess[u] -= send
        excess[v] += send
        if v != source and v != sink and excess[v] == send:
            active.append(v)

    def relabel(u: int) -> None:
        min_h = float("inf")
        for e in graph[u]:
            if e[1] > 0:
                min_h = min(min_h, height[e[0]])
        height[u] = min_h + 1 if min_h < float("inf") else height[u]

    while active:
        u = active.popleft()
        while excess[u] > 0:
            pushed = False
            for e in graph[u]:
                if e[1] > 0 and height[u] == height[e[0]] + 1:
                    push(u, e)
                    pushed = True
                    if excess[u] == 0:
                        break
            if excess[u] > 0:
                relabel(u)
                if not pushed:
                    break
        if excess[u] > 0:
            active.append(u)

    return excess[sink]


if __name__ == "__main__":
    # Classic example
    edges = [(0, 1, 10), (0, 2, 5), (1, 2, 15), (1, 3, 5), (2, 3, 10)]
    flow = max_flow_push_relabel(4, edges, 0, 3)
    assert flow == 15, flow
    print(f"push_relabel flow={flow}")
    print("push_relabel self-tests passed")
