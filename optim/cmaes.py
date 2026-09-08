"""Covariance Matrix Adaptation Evolution Strategy (CMA-ES) simplified full version.

Complexity: O(gens * pop * dim^2). Original implementation.
"""
from __future__ import annotations
import math
import random
from typing import Callable, List, Tuple


def cmaes(
    f: Callable[[List[float]], float],
    x0: List[float],
    sigma0: float = 0.5,
    popsize: int | None = None,
    max_gen: int = 200,
    tol: float = 1e-8,
    seed: int = 42,
) -> Tuple[List[float], float]:
    rng = random.Random(seed)
    n = len(x0)
    if popsize is None:
        popsize = 4 + int(3 * math.log(n))
    mu = popsize // 2
    weights = [math.log(mu + 0.5) - math.log(i + 1) for i in range(mu)]
    wsum = sum(weights)
    weights = [w / wsum for w in weights]
    mueff = 1.0 / sum(w * w for w in weights)

    cc = (4 + mueff / n) / (n + 4 + 2 * mueff / n)
    cs = (mueff + 2) / (n + mueff + 5)
    c1 = 2 / ((n + 1.3) ** 2 + mueff)
    cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((n + 2) ** 2 + mueff))
    damps = 1 + 2 * max(0, math.sqrt((mueff - 1) / (n + 1)) - 1) + cs
    chiN = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n))

    mean = x0[:]
    sigma = sigma0
    C = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    pc = [0.0] * n
    ps = [0.0] * n
    best_x = x0[:]
    best_f = f(x0)

    def matvec(M: List[List[float]], v: List[float]) -> List[float]:
        return [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]

    def cholesky(M: List[List[float]]) -> List[List[float]]:
        L = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                s = sum(L[i][k] * L[j][k] for k in range(j))
                if i == j:
                    val = M[i][i] - s
                    L[i][j] = math.sqrt(max(val, 1e-18))
                else:
                    L[i][j] = (M[i][j] - s) / L[j][j] if L[j][j] > 1e-18 else 0.0
        return L

    for gen in range(max_gen):
        L = cholesky(C)
        population = []
        for _ in range(popsize):
            z = [rng.gauss(0, 1) for _ in range(n)]
            y = matvec(L, z)
            x = [mean[i] + sigma * y[i] for i in range(n)]
            fx = f(x)
            population.append((fx, x, y, z))
            if fx < best_f:
                best_f = fx
                best_x = x[:]
        population.sort(key=lambda t: t[0])
        if best_f < tol:
            break

        # Update mean
        old_mean = mean[:]
        mean = [0.0] * n
        for i in range(mu):
            for d in range(n):
                mean[d] += weights[i] * population[i][1][d]

        # Evolution paths
        invsqrtC_y = [0.0] * n  # approximate using previous
        for i in range(mu):
            for d in range(n):
                invsqrtC_y[d] += weights[i] * population[i][3][d]  # use z as proxy for simplicity in pure impl

        for d in range(n):
            ps[d] = (1 - cs) * ps[d] + math.sqrt(cs * (2 - cs) * mueff) * invsqrtC_y[d]
        hsig = 1.0 if (math.sqrt(sum(p * p for p in ps)) /
                       math.sqrt(1 - (1 - cs) ** (2 * (gen + 1))) / chiN < 1.4 + 2 / (n + 1)) else 0.0
        for d in range(n):
            pc[d] = (1 - cc) * pc[d] + hsig * math.sqrt(cc * (2 - cc) * mueff) * (mean[d] - old_mean[d]) / sigma

        # Update C
        for i in range(n):
            for j in range(n):
                rank1 = pc[i] * pc[j]
                rankmu = sum(weights[k] * population[k][2][i] * population[k][2][j] for k in range(mu))
                C[i][j] = ((1 - c1 - cmu) * C[i][j] + c1 * rank1 + cmu * rankmu)

        # sigma
        ps_norm = math.sqrt(sum(p * p for p in ps))
        sigma *= math.exp((cs / damps) * (ps_norm / chiN - 1))

    return best_x, best_f


if __name__ == "__main__":
    def sphere(x: List[float]) -> float:
        return sum(v * v for v in x)

    x, v = cmaes(sphere, [3.0, -2.0, 1.5], sigma0=1.0, max_gen=80, seed=5)
    assert v < 1e-4, v
    print(f"cmaes best={v:.2e}")
    print("cmaes self-tests passed")
