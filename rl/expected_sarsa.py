"""Expected SARSA."""
from __future__ import annotations
import random
from typing import Callable, List


def expected_sarsa(
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

    def expected_value(s):
        best = max(Q[s])
        n_best = sum(1 for q in Q[s] if q == best)
        ev = 0.0
        for a in range(n_actions):
            if Q[s][a] == best:
                pi = (1 - epsilon) / n_best + epsilon / n_actions
            else:
                pi = epsilon / n_actions
            ev += pi * Q[s][a]
        return ev

    for _ in range(n_episodes):
        s = step_fn("reset")
        done = False
        while not done:
            if rng.random() < epsilon:
                a = rng.randrange(n_actions)
            else:
                a = max(range(n_actions), key=lambda x: Q[s][x])
            ns, r, done = step_fn(a)
            target = r + (0 if done else gamma * expected_value(ns))
            Q[s][a] += alpha * (target - Q[s][a])
            s = ns
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
    Q = expected_sarsa(2, 2, env, n_episodes=200)
    assert Q[0][1] >= Q[0][0]
    print(f"expected_sarsa Q[0]={Q[0]}")
    print("expected_sarsa self-tests passed")
