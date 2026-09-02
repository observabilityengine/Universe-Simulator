"""
Universe Simulator - Simple STRIPS-like Forward Planner
Original state-space search planner.
"""

from __future__ import annotations

from typing import Callable, FrozenSet, List, Optional, Set, Tuple

State = FrozenSet[str]
Action = Tuple[str, FrozenSet[str], FrozenSet[str], FrozenSet[str]]  # name, pre, add, del


def forward_plan(
    start: State,
    goal: State,
    actions: List[Action],
    max_depth: int = 20,
) -> Optional[List[str]]:
    from collections import deque
    queue: deque = deque([(start, [])])
    visited: Set[State] = {start}
    while queue:
        state, path = queue.popleft()
        if goal <= state:
            return path
        if len(path) >= max_depth:
            continue
        for name, pre, add, delete in actions:
            if pre <= state:
                new_state = (state - delete) | add
                fs = frozenset(new_state)
                if fs not in visited:
                    visited.add(fs)
                    queue.append((fs, path + [name]))
    return None


if __name__ == "__main__":
    start = frozenset({"at_A"})
    goal = frozenset({"at_B"})
    actions = [
        ("move_A_B", frozenset({"at_A"}), frozenset({"at_B"}), frozenset({"at_A"})),
        ("move_B_A", frozenset({"at_B"}), frozenset({"at_A"}), frozenset({"at_B"})),
    ]
    plan = forward_plan(start, goal, actions)
    assert plan == ["move_A_B"]
    print("planner self-test passed", plan)
