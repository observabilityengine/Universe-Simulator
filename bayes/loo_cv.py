"""Leave-one-out cross-validation score (importance sampling PSIS-lite)."""
from __future__ import annotations
import math
from typing import Callable, List


def loo_score(log_lik_matrix: List[List[float]]) -> float:
    """log_lik_matrix[i][s] = log p(y_i | theta_s). Returns sum LOO log predictive densities."""
    n = len(log_lik_matrix)
    total = 0.0
    for i in range(n):
        # importance weights proportional to 1/p(y_i|theta)
        logs = log_lik_matrix[i]
        max_l = max(logs)
        weights = [math.exp(-(l - max_l)) for l in logs]
        wsum = sum(weights)
        loo_i = max_l - math.log(wsum / len(logs))
        total += loo_i
    return total


if __name__ == "__main__":
    mat = [[-1.0, -1.1, -0.9], [-2.0, -2.2, -1.8]]
    score = loo_score(mat)
    assert score < 0
    print(f"loo_cv score={score:.3f}")
    print("loo_cv self-tests passed")
