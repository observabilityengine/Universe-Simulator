"""One-step Actor-Critic."""
from __future__ import annotations
import math
import random
from typing import Callable, List


def softmax(logits: List[float]) -> List[float]:
    m = max(logits)
    exps = [math.exp(x - m) for x in logits]
    s = sum(exps)
    return [e / s for e in exps]


def actor_critic(
    n_states: int,
    n_actions: int,
    step_fn: Callable,
    n_episodes: int = 300,
    alpha_theta: float = 0.1,
    alpha_w: float = 0.1,
    gamma: float = 0.99,
    seed: int = 42,
) -> tuple:
    rng = random.Random(seed)
    theta = [[0.0] * n_actions for _ in range(n_states)]
    V = [0.0] * n_states

    for _ in range(n_episodes):
        s = step_fn("reset")
        done = False
        while not done:
            probs = softmax(theta[s])
            a = rng.choices(range(n_actions), weights=probs)[0]
            ns, r, done = step_fn(a)
            delta = r + (0 if done else gamma * V[ns]) - V[s]
            V[s] += alpha_w * delta
            for b in range(n_actions):
                grad = (1 if b == a else 0) - probs[b]
                theta[s][b] += alpha_theta * delta * grad
            s = ns
    return theta, V


if __name__ == "__main__":
    state = [0]
    def env(action):
        if action == "reset":
            state[0] = 0
            return 0
        r = 1.0 if action == 1 else 0.0
        state[0] = 1
        return 1, r, True
    theta, V = actor_critic(2, 2, env, n_episodes=200)
    probs = softmax(theta[0])
    assert probs[1] > 0.4
    print(f"actor_critic probs={probs} V={V}")
    print("actor_critic self-tests passed")
