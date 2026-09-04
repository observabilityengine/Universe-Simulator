"""
Universe Simulator - Gaussian Mixture Model EM
Original 1-D GMM fitting via expectation-maximization.
"""

from __future__ import annotations

import math
from typing import List, Tuple

def gmm_em(data: List[float], n_components: int = 2, max_iter: int = 30) -> Tuple[List[float], List[float], List[float]]:
    n = len(data)
    # init
    weights = [1.0 / n_components] * n_components
    means = [data[i * n // n_components] for i in range(n_components)]
    vars_ = [1.0] * n_components
    for _ in range(max_iter):
        # E-step
        resp = [[0.0]*n_components for _ in range(n)]
        for i, x in enumerate(data):
            dens = []
            for k in range(n_components):
                dens.append(weights[k] * math.exp(-0.5 * (x - means[k])**2 / vars_[k]) / math.sqrt(2 * math.pi * vars_[k]))
            s = sum(dens) + 1e-12
            for k in range(n_components):
                resp[i][k] = dens[k] / s
        # M-step
        for k in range(n_components):
            nk = sum(resp[i][k] for i in range(n)) + 1e-12
            weights[k] = nk / n
            means[k] = sum(resp[i][k] * data[i] for i in range(n)) / nk
            vars_[k] = sum(resp[i][k] * (data[i] - means[k])**2 for i in range(n)) / nk + 1e-6
    return weights, means, vars_

if __name__ == "__main__":
    data = [0.1, 0.2, 0.15, 5.0, 5.1, 5.2, 5.3]
    w, m, v = gmm_em(data, 2)
    assert abs(m[0] - m[1]) > 2.0
    print("gmm_em self-test passed", m)
