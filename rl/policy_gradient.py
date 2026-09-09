"""REINFORCE policy gradient for discrete actions."""
from __future__ import annotations
import math
import random
from typing import Callable, List, Tuple


def softmax(logits: List[float]) -> List[float]:
    m = max(logits)
    exps = [math.exp(x - m) for x in logits]
    s = sum(exps)
    return [e / s for e in exps]


def reinforce(
    n_states: int,
    n_actions: int,
    step_fn: Callable,
    n_episodes: int = 300,
    gamma: float = 0.99,
    lr: float = 0.1,
    seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    theta = [[0.0] * n_actions for _ in range(n_states)]

    for _ in range(n_episodes):
        s = step_fn("reset")
        episode = []
        done = False
        while not done:
            probs = softmax(theta[s])
            a = rng.choices(range(n_actions), weights=probs)[0]
            ns, r, done = step_fn(a)
            episode.append((s, a, r))
            s = ns
        G = 0.0
        for t in range(len(episode) - 1, -1, -1):
            s, a, r = episode[t]
            G = gamma * G + r
            probs = softmax(theta[s])
            for b in range(n_actions):
                grad = (1 if b == a else 0) - probs[b]
                theta[s][b] += lr * G * grad
    return theta


if __name__ == "__main__":
    state = [0]
    def env(action):
        if action == "reset":
            state[0] = 0
            return 0
        r = 1.0 if action == 1 else 0.0
        state[0] = 1
        return 1, r, True
    theta = reinforce(2, 2, env, n_episodes=200)
    probs = softmax(theta[0])
    assert probs[1] > probs[0]
    print(f"policy_gradient probs={probs}")
    print("policy_gradient self-tests passed")
