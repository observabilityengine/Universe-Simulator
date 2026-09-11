"""Weight initialization schemes."""
from __future__ import annotations
import math
import random
from .tensor import Tensor


def xavier_uniform(rows: int, cols: int, seed: int = 42) -> Tensor:
    rng = random.Random(seed)
    limit = math.sqrt(6.0 / (rows + cols))
    return Tensor([[rng.uniform(-limit, limit) for _ in range(cols)] for _ in range(rows)], requires_grad=True)


def he_normal(rows: int, cols: int, seed: int = 42) -> Tensor:
    rng = random.Random(seed)
    std = math.sqrt(2.0 / rows)
    return Tensor([[rng.gauss(0, std) for _ in range(cols)] for _ in range(rows)], requires_grad=True)


def zeros(rows: int, cols: int) -> Tensor:
    return Tensor([[0.0] * cols for _ in range(rows)], requires_grad=True)


if __name__ == "__main__":
    w = xavier_uniform(10, 5)
    assert w.shape == (10, 5)
    h = he_normal(10, 5)
    print(f"init_weights xavier_range~{max(abs(x) for row in w.data for x in row):.3f}")
    print("init_weights self-tests passed")
