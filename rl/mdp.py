"""Markov Decision Process representation."""
from __future__ import annotations
from typing import Dict, List, Tuple

State = int
Action = int


class MDP:
    def __init__(self, n_states: int, n_actions: int, gamma: float = 0.99):
        self.n_states = n_states
        self.n_actions = n_actions
        self.gamma = gamma
        self.P: Dict[Tuple[State, Action], List[Tuple[float, State, float]]] = {}

    def set_transition(self, s: State, a: Action, outcomes: List[Tuple[float, State, float]]) -> None:
        self.P[(s, a)] = outcomes

    def transitions(self, s: State, a: Action):
        return self.P.get((s, a), [])


def gridworld_mdp(size: int = 4, gamma: float = 0.9) -> MDP:
    mdp = MDP(size * size, 4, gamma)
    goal = size * size - 1
    for s in range(size * size):
        if s == goal:
            for a in range(4):
                mdp.set_transition(s, a, [(1.0, s, 0.0)])
            continue
        r, c = divmod(s, size)
        for a, (dr, dc) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                ns = nr * size + nc
                reward = 1.0 if ns == goal else -0.01
                mdp.set_transition(s, a, [(1.0, ns, reward)])
            else:
                mdp.set_transition(s, a, [(1.0, s, -0.1)])
    return mdp


if __name__ == "__main__":
    m = gridworld_mdp(3)
    assert m.n_states == 9
    assert len(m.transitions(0, 0)) >= 1
    print("mdp self-tests passed")
