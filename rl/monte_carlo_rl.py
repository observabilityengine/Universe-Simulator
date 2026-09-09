"""Monte Carlo first-visit control."""
from __future__ import annotations
import random
from typing import Callable, Dict, List, Tuple


def mc_control(
    n_states: int,
    n_actions: int,
    step_fn: Callable,
    n_episodes: int = 500,
    gamma: float = 0.99,
    epsilon: float = 0.1,
    seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    Q = [[0.0] * n_actions for _ in range(n_states)]
    returns: Dict[Tuple[int, int], List[float]] = {}

    def policy(s):
        if rng.random() < epsilon:
            return rng.randrange(n_actions)
        return max(range(n_actions), key=lambda x: Q[s][x])

    for _ in range(n_episodes):
        s = step_fn("reset")
        episode = []
        done = False
        while not done:
            a = policy(s)
            ns, r, done = step_fn(a)
            episode.append((s, a, r))
            s = ns
        G = 0.0
        visited = set()
        for t in range(len(episode) - 1, -1, -1):
            s, a, r = episode[t]
            G = gamma * G + r
            if (s, a) not in visited:
                visited.add((s, a))
                returns.setdefault((s, a), []).append(G)
                Q[s][a] = sum(returns[(s, a)]) / len(returns[(s, a)])
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
    Q = mc_control(2, 2, env, n_episodes=300)
    assert Q[0][1] >= Q[0][0]
    print(f"monte_carlo_rl Q[0]={Q[0]}")
    print("monte_carlo_rl self-tests passed")
