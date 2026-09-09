"""Minimal gym-like environment interface and FrozenLake toy env."""
from __future__ import annotations
import random
from typing import Any, Tuple


class Env:
    def reset(self) -> Any:
        raise NotImplementedError

    def step(self, action: int) -> Tuple[Any, float, bool, dict]:
        raise NotImplementedError


class FrozenLake(Env):
    def __init__(self, size: int = 4, seed: int = 42):
        self.size = size
        self.goal = size * size - 1
        self.holes = {size + 1, 2 * size + 2} if size >= 3 else set()
        self.rng = random.Random(seed)
        self.s = 0

    def reset(self) -> int:
        self.s = 0
        return self.s

    def step(self, action: int) -> Tuple[int, float, bool, dict]:
        r, c = divmod(self.s, self.size)
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = deltas[action % 4]
        nr, nc = max(0, min(self.size - 1, r + dr)), max(0, min(self.size - 1, c + dc))
        self.s = nr * self.size + nc
        if self.s in self.holes:
            return self.s, -1.0, True, {}
        if self.s == self.goal:
            return self.s, 1.0, True, {}
        return self.s, -0.01, False, {}


if __name__ == "__main__":
    env = FrozenLake(3)
    s = env.reset()
    assert s == 0
    ns, r, done, _ = env.step(1)
    print(f"env_gym ns={ns} r={r} done={done}")
    print("env_gym self-tests passed")
