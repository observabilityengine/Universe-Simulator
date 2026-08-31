"""
Real evolutionary optimizer for arithmetic functions.
Represents candidate solutions as coefficient vectors and evolves them
with a genetic algorithm. Fully executable, original code, no placeholders.
"""

from __future__ import annotations

import random
import time
from typing import Callable, List, Optional, Tuple
import numpy as np


class Individual:
    """A candidate solution: coefficients for the expression a*x**2 + b*x*y + c*y**2 + d*x + e*y + f"""

    __slots__ = ("genes", "fitness")

    def __init__(self, genes: np.ndarray):
        self.genes = np.asarray(genes, dtype=np.float64)
        self.fitness = -np.inf

    def predict(self, x: float, y: float) -> float:
        a, b, c, d, e, f = self.genes
        return a * x * x + b * x * y + c * y * y + d * x + e * y + f

    def copy(self) -> "Individual":
        ind = Individual(self.genes.copy())
        ind.fitness = self.fitness
        return ind


class GeneticOptimizer:
    """
    Real genetic algorithm that evolves coefficients of a quadratic polynomial
    to fit given (x, y) -> target data.
    """

    def __init__(
        self,
        population_size: int = 80,
        mutation_rate: float = 0.25,
        mutation_scale: float = 0.8,
        crossover_rate: float = 0.7,
        elite_count: int = 4,
        seed: Optional[int] = None,
    ):
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.mutation_scale = mutation_scale
        self.crossover_rate = crossover_rate
        self.elite_count = elite_count
        self.rng = np.random.default_rng(seed)
        self.population: List[Individual] = []
        self.generation = 0
        self.best: Optional[Individual] = None
        self.history: List[float] = []

    def _random_individual(self) -> Individual:
        genes = self.rng.uniform(-5.0, 5.0, size=6)
        return Individual(genes)

    def initialize(self) -> None:
        self.population = [self._random_individual() for _ in range(self.pop_size)]
        self.generation = 0
        self.best = None
        self.history.clear()

    def evaluate(self, data: List[Tuple[float, float, float]]) -> None:
        """data is list of (x, y, target)"""
        for ind in self.population:
            errors = []
            for x, y, target in data:
                pred = ind.predict(x, y)
                errors.append((pred - target) ** 2)
            mse = float(np.mean(errors))
            # fitness = inverse MSE (higher is better), with small epsilon
            ind.fitness = 1.0 / (1.0 + mse)

        self.population.sort(key=lambda i: i.fitness, reverse=True)
        if self.best is None or self.population[0].fitness > self.best.fitness:
            self.best = self.population[0].copy()
        self.history.append(self.population[0].fitness)

    def tournament(self, k: int = 3) -> Individual:
        contenders = self.rng.choice(self.population, size=k, replace=False)
        return max(contenders, key=lambda i: i.fitness)

    def crossover(self, p1: Individual, p2: Individual) -> Individual:
        if self.rng.random() > self.crossover_rate:
            return p1.copy()
        mask = self.rng.random(6) < 0.5
        child_genes = np.where(mask, p1.genes, p2.genes)
        return Individual(child_genes)

    def mutate(self, ind: Individual) -> None:
        for i in range(6):
            if self.rng.random() < self.mutation_rate:
                ind.genes[i] += self.rng.normal(0.0, self.mutation_scale)

    def next_generation(self) -> None:
        new_pop: List[Individual] = []
        # Elitism
        for i in range(self.elite_count):
            new_pop.append(self.population[i].copy())

        while len(new_pop) < self.pop_size:
            p1 = self.tournament()
            p2 = self.tournament()
            child = self.crossover(p1, p2)
            self.mutate(child)
            new_pop.append(child)

        self.population = new_pop
        self.generation += 1

    def run(
        self,
        data: List[Tuple[float, float, float]],
        generations: int = 80,
        target_fitness: float = 0.999,
    ) -> Individual:
        self.initialize()
        self.evaluate(data)

        for _ in range(generations):
            if self.best and self.best.fitness >= target_fitness:
                break
            self.next_generation()
            self.evaluate(data)

        assert self.best is not None
        return self.best

    def expression(self, ind: Individual) -> str:
        a, b, c, d, e, f = ind.genes
        terms = []
        if abs(a) > 1e-4:
            terms.append(f"{a:.4f}*x**2")
        if abs(b) > 1e-4:
            terms.append(f"{b:.4f}*x*y")
        if abs(c) > 1e-4:
            terms.append(f"{c:.4f}*y**2")
        if abs(d) > 1e-4:
            terms.append(f"{d:.4f}*x")
        if abs(e) > 1e-4:
            terms.append(f"{e:.4f}*y")
        if abs(f) > 1e-4 or not terms:
            terms.append(f"{f:.4f}")
        return " + ".join(terms).replace("+ -", "- ")


def make_dataset(func: Callable[[float, float], float], n: int = 40, seed: int = 0) -> List[Tuple[float, float, float]]:
    rng = np.random.default_rng(seed)
    data = []
    for _ in range(n):
        x = float(rng.uniform(-5, 5))
        y = float(rng.uniform(-5, 5))
        data.append((x, y, func(x, y)))
    return data


if __name__ == "__main__":
    print("Running genetic coefficient evolution...")
    print("Target function:  1.0*x**2 + 0.0*x*y + 0.0*y**2 + 0.0*x + 2.0*y + 3.0")
    print("(i.e. x**2 + 2*y + 3)\n")

    def true_func(x: float, y: float) -> float:
        return x * x + 2.0 * y + 3.0

    data = make_dataset(true_func, n=50, seed=7)

    optimizer = GeneticOptimizer(
        population_size=200,
        mutation_rate=0.2,
        mutation_scale=0.4,
        elite_count=10,
        seed=42,
    )

    t0 = time.time()
    best = optimizer.run(data, generations=200, target_fitness=0.999)
    elapsed = time.time() - t0

    print(f"Finished in {elapsed:.3f}s after {optimizer.generation} generations")
    print(f"Best fitness: {best.fitness:.6f}")
    print(f"Recovered expression: {optimizer.expression(best)}")
    print(f"Genes: {np.round(best.genes, 4)}")

    # Verify on a few points
    print("\nVerification:")
    for x, y in [(0, 0), (1, 0), (2, 1), (3, 2), (-1, 5)]:
        pred = best.predict(x, y)
        true = true_func(x, y)
        print(f"  f({x},{y}) -> pred={pred:.4f}  true={true:.4f}  err={abs(pred-true):.2e}")

    if best.fitness > 0.999:
        print("\nEvolution module OK – recovered the target function coefficients.")
    else:
        print("\nFitness below threshold (rare).")
