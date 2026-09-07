"""Nelder-Mead simplex optimizer.

Complexity: O(iters * dim). Original implementation.
"""
from __future__ import annotations
from typing import Callable, List, Tuple

def nelder_mead(
    f: Callable[[List[float]], float],
    x0: List[float],
    max_iter: int = 200,
    tol: float = 1e-6,
    alpha: float = 1.0,
    gamma: float = 2.0,
    rho: float = 0.5,
    sigma: float = 0.5,
) -> Tuple[List[float], float]:
    n = len(x0)
    simplex = [x0[:]]
    for i in range(n):
        pt = x0[:]
        pt[i] += 0.05 if x0[i] == 0 else 0.05 * abs(x0[i])
        simplex.append(pt)
    scores = [f(p) for p in simplex]
    for _ in range(max_iter):
        order = sorted(range(n+1), key=lambda i: scores[i])
        simplex = [simplex[i] for i in order]
        scores = [scores[i] for i in order]
        cent = [sum(simplex[i][j] for i in range(n))/n for j in range(n)]
        xr = [cent[j] + alpha*(cent[j]-simplex[-1][j]) for j in range(n)]
        fr = f(xr)
        if scores[0] <= fr < scores[-2]:
            simplex[-1], scores[-1] = xr, fr
        elif fr < scores[0]:
            xe = [cent[j] + gamma*(xr[j]-cent[j]) for j in range(n)]
            fe = f(xe)
            if fe < fr:
                simplex[-1], scores[-1] = xe, fe
            else:
                simplex[-1], scores[-1] = xr, fr
        else:
            xc = [cent[j] + rho*(simplex[-1][j]-cent[j]) for j in range(n)]
            fc = f(xc)
            if fc < scores[-1]:
                simplex[-1], scores[-1] = xc, fc
            else:
                for i in range(1, n+1):
                    simplex[i] = [simplex[0][j] + sigma*(simplex[i][j]-simplex[0][j]) for j in range(n)]
                    scores[i] = f(simplex[i])
        if max(scores) - min(scores) < tol:
            break
    best = min(range(n+1), key=lambda i: scores[i])
    return simplex[best], scores[best]

if __name__ == "__main__":
    def rosen(x):
        return (1-x[0])**2 + 100*(x[1]-x[0]**2)**2
    x, v = nelder_mead(rosen, [-1.0, 1.0], max_iter=300)
    assert v < 1e-3, v
    print("nelder_mead self-tests passed")
