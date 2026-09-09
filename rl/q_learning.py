"""Tabular Q-learning."""
from __future__ import annotations
import random
from typing import Callable, List, Tuple


def q_learning(
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
    for _ in range(n_episodes):
        s = step_fn("reset")
        done = False
        while not done:
            if rng.random() < epsilon:
                a = rng.randrange(n_actions)
            else:
                a = max(range(n_actions), key=lambda x: Q[s][x])
            ns, r, done = step_fn(a)
            best_next = max(Q[ns]) if not done else 0.0
            Q[s][a] += alpha * (r + gamma * best_next - Q[s][a])
            s = ns
    return Q


if __name__ == "__main__":
    # Simple 2-state bandit-like
    state = [0]
    def env(action):
        if action == "reset":
            state[0] = 0
            return 0
        r = 1.0 if action == 1 else 0.0
        state[0] = 1
        return 1, r, True
    Q = q_learning(2, 2, env, n_episodes=200)
    assert Q[0][1] > Q[0][0]
    print(f"q_learning Q[0]={Q[0]}")
    print("q_learning self-tests passed")
