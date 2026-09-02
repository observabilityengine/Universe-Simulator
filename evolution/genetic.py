"""
Universe Simulator - Simple Genetic Algorithm
Original bitstring GA for maximising 1-bits (OneMax).
"""

from __future__ import annotations

import random
from typing import List


def onemax(bits: List[int]) -> int:
    return sum(bits)


def genetic(
    length: int = 20,
    pop_size: int = 30,
    generations: int = 40,
    mutation_rate: float = 0.02,
    seed: int = 42,
) -> List[int]:
    rng = random.Random(seed)
    pop = [[rng.randint(0, 1) for _ in range(length)] for _ in range(pop_size)]

    for _ in range(generations):
        scored = [(onemax(ind), ind) for ind in pop]
        scored.sort(reverse=True)
        survivors = [ind for _, ind in scored[: pop_size // 2]]
        children = []
        while len(children) + len(survivors) < pop_size:
            p1, p2 = rng.sample(survivors, 2)
            cut = rng.randint(1, length - 1)
            child = p1[:cut] + p2[cut:]
            for i in range(length):
                if rng.random() < mutation_rate:
                    child[i] = 1 - child[i]
            children.append(child)
        pop = survivors + children
    best = max(pop, key=onemax)
    return best


if __name__ == "__main__":
    best = genetic()
    assert onemax(best) >= 15
    print("genetic self-test passed", onemax(best), best)
