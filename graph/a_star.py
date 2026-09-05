"""A* shortest path with heuristic.

Complexity: O((V + E) log V) with binary heap, assuming consistent heuristic.
Requires non-negative weights + admissible heuristic.
Returns path cost or INF if unreachable. Path reconstruction optional.
"""
from __future__ import annotations

import heapq
from typing import Dict, List, Tuple, Callable, Optional

INF = float("inf")


def a_star(
    graph: Dict[int, List[Tuple[int, float]]],
    start: int,
    goal: int,
    heuristic: Callable[[int, int], float],
) -> float:
    """A* distance from start to goal.

    Parameters
    ----------
    graph : adj list node -> [(nei, weight), ...]
    start, goal : nodes
    heuristic : h(u, goal) estimated cost; must be admissible

    Returns
    -------
    shortest path cost or INF if unreachable
    """
    if start == goal:
        return 0.0
    open_set: List[Tuple[float, float, int]] = []  # (f, g, node)
    heapq.heappush(open_set, (heuristic(start, goal), 0.0, start))
    g_score: Dict[int, float] = {start: 0.0}
    closed: set[int] = set()

    while open_set:
        f, g, u = heapq.heappop(open_set)
        if u in closed:
            continue
        if u == goal:
            return g
        closed.add(u)
        for v, w in graph.get(u, []):
            if w < 0:
                raise ValueError("A* requires non-negative weights")
            if v in closed:
                continue
            tentative = g + w
            if tentative < g_score.get(v, INF):
                g_score[v] = tentative
                f_score = tentative + heuristic(v, goal)
                heapq.heappush(open_set, (f_score, tentative, v))
    return INF


if __name__ == "__main__":
    # Grid-like with manhattan heuristic
    g = {
        0: [(1, 1.0), (2, 1.0)],
        1: [(0, 1.0), (3, 1.0)],
        2: [(0, 1.0), (3, 1.0)],
        3: [(1, 1.0), (2, 1.0)],
    }
    def h(u, goal):
        # trivial zero heuristic (degenerates to Dijkstra)
        return 0.0
    assert abs(a_star(g, 0, 3, h) - 2.0) < 1e-9

    # Unreachable
    g2 = {0: [(1, 1.0)], 1: [], 2: []}
    assert a_star(g2, 0, 2, h) == INF

    # Start == goal
    assert a_star({0: []}, 0, 0, h) == 0.0

    # Negative weight raises
    try:
        a_star({0: [(1, -1.0)]}, 0, 1, h)
        assert False
    except ValueError:
        pass

    print("a_star self-tests passed")
