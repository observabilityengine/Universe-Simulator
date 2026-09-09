"""Temporal-Difference TD(0) prediction."""
from __future__ import annotations
import random
from typing import Callable, List


def td0(
    n_states: int,
    step_fn: Callable,
    policy: Callable[[int], int],
    n_episodes: int = 500,
    alpha: float = 0.1,
    gamma: float = 0.99,
    seed: int = 42,
) -> List[float]:
    rng = random.Random(seed)
    V = [0.0] * n_states
    for _ in range(n_episodes):
        s = step_fn("reset")
        done = False
        while not done:
            a = policy(s)
            ns, r, done = step_fn(a)
            V[s] += alpha * (r + gamma * (0 if done else V[ns]) - V[s])
            s = ns
    return V


if __name__ == "__main__":
    state = [0]
    def env(a):
        if a == "reset":
            state[0] = 0
            return 0
        state[0] = 1
        return 1, 1.0, True
    V = td0(2, env, lambda s: 0, n_episodes=100)
    assert V[0] > 0
    print(f"td_learning V={V}")
    print("td_learning self-tests passed")
