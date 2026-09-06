"""Floyd's cycle-finding algorithm (tortoise and hare).

Complexity: O(μ + λ) where μ is start of cycle, λ is cycle length.
Works on functional graphs via next_fn. Returns (cycle_start_index, cycle_length)
or (None, 0) if no cycle. Original implementation.
"""
from __future__ import annotations

from typing import Callable, Hashable, Optional, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


def floyd_cycle(
    start: T,
    next_fn: Callable[[T], T],
    max_steps: int = 1_000_000,
) -> Tuple[Optional[int], int]:
    """Detect cycle. Returns (mu, lambda) or (None, 0) if acyclic within max_steps."""
    tortoise = next_fn(start)
    hare = next_fn(next_fn(start))
    steps = 0
    while tortoise != hare:
        tortoise = next_fn(tortoise)
        hare = next_fn(next_fn(hare))
        steps += 1
        if steps > max_steps:
            return None, 0
    # find start of cycle
    mu = 0
    tortoise = start
    while tortoise != hare:
        tortoise = next_fn(tortoise)
        hare = next_fn(hare)
        mu += 1
    # find cycle length
    lam = 1
    hare = next_fn(tortoise)
    while tortoise != hare:
        hare = next_fn(hare)
        lam += 1
    return mu, lam


if __name__ == "__main__":
    # sequence: 0→1→2→3→4→2→3→4→...
    succ = {0: 1, 1: 2, 2: 3, 3: 4, 4: 2}
    mu, lam = floyd_cycle(0, lambda x: succ[x])
    assert mu == 2 and lam == 3
    # no cycle within chain
    chain = {i: i + 1 for i in range(10)}
    chain[10] = 10  # self-loop at end
    mu2, lam2 = floyd_cycle(0, lambda x: chain[x])
    assert mu2 == 10 and lam2 == 1
    print("floyd_cycle self-tests passed")
