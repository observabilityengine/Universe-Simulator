"""
Universe Simulator - IDA* (Iterative Deepening A*)
Original implementation for unit-cost graphs.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple, TypeVar

T = TypeVar("T")


def ida_star(
    start: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[Tuple[T, float]]],
    heuristic: Callable[[T], float],
    max_depth: int = 100,
) -> Optional[List[T]]:
    bound = heuristic(start)

    def search(path: List[T], g: float, bound: float) -> Tuple[float, Optional[List[T]]]:
        node = path[-1]
        f = g + heuristic(node)
        if f > bound:
            return f, None
        if goal_test(node):
            return f, path
        min_t = float("inf")
        for nxt, cost in successors(node):
            if nxt in path:
                continue
            t, res = search(path + [nxt], g + cost, bound)
            if res is not None:
                return t, res
            if t < min_t:
                min_t = t
        return min_t, None

    for _ in range(max_depth):
        t, result = search([start], 0.0, bound)
        if result is not None:
            return result
        if t == float("inf"):
            return None
        bound = t
    return None


if __name__ == "__main__":
    # 1-D path to 5
    def succ(x):
        return [(x+1, 1.0), (x+2, 1.5)] if x < 5 else []
    path = ida_star(0, lambda x: x >= 5, succ, lambda x: max(0, 5-x))
    assert path is not None and path[-1] >= 5
    print("ida_star self-test passed", path)
