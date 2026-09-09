"""Tabular SARSA."""
from __future__ import annotations
import random
from typing import Callable, List


def sarsa(
    n_states: int,
    n_actions: int,
    step_fn: Callable,
    n_episodes: int = 500,
    alpha: float = 0.1,
    gamma: float = 0.99,
    epsilon: float = 0.1,
    seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    Q = [[0.0] * n_actions for _ in range(n_states)]

    def policy(s):
        if rng.random() < epsilon:
            return rng.randrange(n_actions)
        return max(range(n_actions), key=lambda x: Q[s][x])

    for _ in range(n_episodes):
        s = step_fn("reset")
        a = policy(s)
        done = False
        while not done:
            ns, r, done = step_fn(a)
            na = policy(ns) if not done else 0
            Q[s][a] += alpha * (r + gamma * (Q[ns][na] if not done else 0) - Q[s][a])
            s, a = ns, na
    return Q


if __name__ == "__main__":
    state = [0]
    def env(action):
        if action == "reset":
            state[0] = 0
            return 0
        r = 1.0 if action == 1 else 0.0
        state[0] = 1
        return 1, r, True
    Q = sarsa(2, 2, env, n_episodes=200)
    assert Q[0][1] >= Q[0][0]
    print(f"sarsa Q[0]={Q[0]}")
    print("sarsa self-tests passed")
