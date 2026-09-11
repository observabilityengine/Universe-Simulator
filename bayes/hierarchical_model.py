"""Simple hierarchical normal model (empirical Bayes)."""
from __future__ import annotations
from typing import List, Tuple


def fit_hierarchical(group_means: List[float], group_vars: List[float], group_ns: List[int]) -> Tuple[float, float, List[float]]:
    """Estimate global mean and shrinkage estimates."""
    k = len(group_means)
    # Grand mean
    mu = sum(m * n for m, n in zip(group_means, group_ns)) / sum(group_ns)
    # Between variance (method of moments)
    between = max(0.0, sum(n * (m - mu) ** 2 for m, n in zip(group_means, group_ns)) / k - sum(group_vars) / k)
    # Shrinkage
    shrunk = []
    for m, v, n in zip(group_means, group_vars, group_ns):
        se2 = v / n
        B = se2 / (se2 + between + 1e-12)
        shrunk.append((1 - B) * m + B * mu)
    return mu, between, shrunk


if __name__ == "__main__":
    means = [1.0, 2.0, 1.5, 3.0]
    vars_ = [1.0, 1.0, 1.0, 1.0]
    ns = [10, 10, 10, 10]
    mu, tau, shrunk = fit_hierarchical(means, vars_, ns)
    assert abs(mu - 1.875) < 0.1
    print(f"hierarchical_model mu={mu:.3f} shrunk={shrunk}")
    print("hierarchical_model self-tests passed")
