"""Minimal DQN with linear function approximation and replay buffer."""
from __future__ import annotations
import random
from typing import Callable, List, Tuple


class ReplayBuffer:
    def __init__(self, capacity: int = 1000):
        self.buf: List[Tuple] = []
        self.capacity = capacity

    def push(self, transition):
        if len(self.buf) >= self.capacity:
            self.buf.pop(0)
        self.buf.append(transition)

    def sample(self, n: int, rng):
        return rng.sample(self.buf, min(n, len(self.buf)))


def dqn_linear(
    n_features: int,
    n_actions: int,
    step_fn: Callable,
    featurize: Callable,
    n_episodes: int = 200,
    alpha: float = 0.01,
    gamma: float = 0.99,
    epsilon: float = 0.1,
    seed: int = 42,
) -> List[List[float]]:
    rng = random.Random(seed)
    W = [[0.0] * n_features for _ in range(n_actions)]
    buf = ReplayBuffer()

    def q(s_feat, a):
        return sum(W[a][i] * s_feat[i] for i in range(n_features))

    for _ in range(n_episodes):
        s = step_fn("reset")
        done = False
        while not done:
            feat = featurize(s)
            if rng.random() < epsilon:
                a = rng.randrange(n_actions)
            else:
                a = max(range(n_actions), key=lambda x: q(feat, x))
            ns, r, done = step_fn(a)
            buf.push((feat, a, r, featurize(ns), done))
            for feat_b, a_b, r_b, nfeat_b, done_b in buf.sample(8, rng):
                target = r_b + (0 if done_b else gamma * max(q(nfeat_b, a2) for a2 in range(n_actions)))
                err = target - q(feat_b, a_b)
                for i in range(n_features):
                    W[a_b][i] += alpha * err * feat_b[i]
            s = ns
    return W


if __name__ == "__main__":
    state = [0]
    def env(action):
        if action == "reset":
            state[0] = 0
            return 0
        r = 1.0 if action == 1 else 0.0
        state[0] = 1
        return 1, r, True
    def feat(s):
        return [1.0, float(s)]
    W = dqn_linear(2, 2, env, feat, n_episodes=100)
    print(f"dqn W[0]={W[0]} W[1]={W[1]}")
    print("dqn self-tests passed")
