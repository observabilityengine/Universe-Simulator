"""
Universe Simulator - Beam Search
Original generic beam search over expandable states.
"""

from __future__ import annotations

from typing import Callable, List, Tuple, TypeVar

T = TypeVar("T")


def beam_search(
    start: T,
    expand: Callable[[T], List[Tuple[T, float]]],
    is_goal: Callable[[T], bool],
    beam_width: int = 3,
    max_steps: int = 20,
) -> T | None:
    beam: List[Tuple[T, float]] = [(start, 0.0)]
    for _ in range(max_steps):
        candidates: List[Tuple[T, float]] = []
        for state, score in beam:
            if is_goal(state):
                return state
            for nxt, cost in expand(state):
                candidates.append((nxt, score + cost))
        if not candidates:
            break
        candidates.sort(key=lambda x: x[1])
        beam = candidates[:beam_width]
    for state, _ in beam:
        if is_goal(state):
            return state
    return None


if __name__ == "__main__":
    # shortest path on line 0 -> 5
    def expand(x):
        return [(x + 1, 1.0), (x + 2, 1.5)] if x < 5 else []
    goal = beam_search(0, expand, lambda x: x >= 5, beam_width=2)
    assert goal is not None and goal >= 5
    print("beam_search self-test passed", goal)
