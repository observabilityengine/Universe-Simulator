"""
Module 65 – Topological Sort
Kahn's algorithm for DAG topological ordering.
Complete implementation.
"""

from __future__ import annotations
from collections import deque, defaultdict
from typing import Dict, List, Hashable, Optional, Set


def topological_sort(edges: List[tuple]) -> Optional[List[Hashable]]:
    graph: Dict[Hashable, List[Hashable]] = defaultdict(list)
    indegree: Dict[Hashable, int] = defaultdict(int)
    nodes: Set[Hashable] = set()
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
        nodes.add(u)
        nodes.add(v)
        if u not in indegree:
            indegree[u] = indegree.get(u, 0)
    queue = deque([n for n in nodes if indegree[n] == 0])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(order) != len(nodes):
        return None
    return order


if __name__ == "__main__":
    print("Testing Topological Sort...")
    edges = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e")]
    order = topological_sort(edges)
    print(f"  Order: {order}")
    cycle_edges = edges + [("e", "a")]
    print(f"  With cycle: {topological_sort(cycle_edges)}")
    print("Topological Sort module OK.")
