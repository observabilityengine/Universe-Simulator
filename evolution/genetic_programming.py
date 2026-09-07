"""Simple Genetic Programming (expression trees for symbolic regression).

Complexity: O(pop * depth * gens). Original implementation.
"""
from __future__ import annotations

import math
import random
from typing import List, Tuple, Union

Node = Union[str, float, Tuple[str, "Node", "Node"], Tuple[str, "Node"]]


def genetic_programming(
    X: List[List[float]],
    y: List[float],
    generations: int = 30,
    pop_size: int = 40,
    max_depth: int = 4,
    seed: int = 42,
) -> Tuple[Node, float]:
    """Evolve expression tree to fit X -> y. Returns (best_tree, mse)."""
    rng = random.Random(seed)
    n_features = len(X[0]) if X else 1
    terminals = [f"x{i}" for i in range(n_features)] + [0.5, 1.0, 2.0, -1.0]
    functions = ["+", "-", "*", "sin", "cos"]

    def random_tree(depth: int = 0) -> Node:
        if depth >= max_depth or (depth > 0 and rng.random() < 0.4):
            return rng.choice(terminals)
        op = rng.choice(functions)
        if op in ("sin", "cos"):
            return (op, random_tree(depth + 1))
        return (op, random_tree(depth + 1), random_tree(depth + 1))

    def eval_tree(tree: Node, row: List[float]) -> float:
        if isinstance(tree, (int, float)):
            return float(tree)
        if isinstance(tree, str) and tree.startswith("x"):
            idx = int(tree[1:])
            return row[idx] if idx < len(row) else 0.0
        if isinstance(tree, tuple):
            op = tree[0]
            if op in ("sin", "cos"):
                v = eval_tree(tree[1], row)
                return math.sin(v) if op == "sin" else math.cos(v)
            a = eval_tree(tree[1], row)
            b = eval_tree(tree[2], row)
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
        return 0.0

    def mse(tree: Node) -> float:
        err = 0.0
        for row, target in zip(X, y):
            try:
                pred = eval_tree(tree, row)
                if math.isnan(pred) or math.isinf(pred):
                    return 1e6
                err += (pred - target) ** 2
            except Exception:
                return 1e6
        return err / max(1, len(X))

    def mutate(tree: Node, depth: int = 0) -> Node:
        if rng.random() < 0.2 or depth >= max_depth:
            return random_tree(depth)
        if isinstance(tree, tuple):
            if tree[0] in ("sin", "cos"):
                return (tree[0], mutate(tree[1], depth + 1))
            return (tree[0], mutate(tree[1], depth + 1), mutate(tree[2], depth + 1))
        return tree

    def crossover(t1: Node, t2: Node) -> Node:
        if rng.random() < 0.5:
            return t1
        return t2

    pop = [random_tree() for _ in range(pop_size)]
    fitness = [mse(t) for t in pop]
    best_idx = min(range(pop_size), key=lambda i: fitness[i])
    best = pop[best_idx]
    best_fit = fitness[best_idx]

    for _ in range(generations):
        new_pop = [best]
        while len(new_pop) < pop_size:
            i1 = min(rng.sample(range(pop_size), 3), key=lambda i: fitness[i])
            i2 = min(rng.sample(range(pop_size), 3), key=lambda i: fitness[i])
            child = crossover(pop[i1], pop[i2])
            child = mutate(child)
            new_pop.append(child)
        pop = new_pop
        fitness = [mse(t) for t in pop]
        idx = min(range(pop_size), key=lambda i: fitness[i])
        if fitness[idx] < best_fit:
            best = pop[idx]
            best_fit = fitness[idx]
    return best, best_fit


if __name__ == "__main__":
    X = [[float(i)] for i in range(-5, 6)]
    y = [x[0] + 1 for x in X]
    tree, err = genetic_programming(X, y, generations=20, pop_size=30, seed=15)
    assert err < 5.0
    print("genetic_programming self-tests passed")
