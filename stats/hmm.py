"""Hidden Markov Model — forward-backward and Viterbi.

Complexity: O(T N^2). Original implementation.
"""
from __future__ import annotations
import math
from typing import List, Tuple

def forward(
    observations: List[int],
    transition: List[List[float]],
    emission: List[List[float]],
    start: List[float],
) -> Tuple[List[List[float]], float]:
    T = len(observations)
    N = len(start)
    alpha = [[0.0] * N for _ in range(T)]
    c0 = 0.0
    for j in range(N):
        alpha[0][j] = start[j] * emission[j][observations[0]]
        c0 += alpha[0][j]
    if c0 > 0:
        for j in range(N):
            alpha[0][j] /= c0
    loglik = math.log(c0) if c0 > 0 else -1e300
    for t in range(1, T):
        ct = 0.0
        for j in range(N):
            s = sum(alpha[t - 1][i] * transition[i][j] for i in range(N))
            alpha[t][j] = s * emission[j][observations[t]]
            ct += alpha[t][j]
        if ct > 0:
            for j in range(N):
                alpha[t][j] /= ct
            loglik += math.log(ct)
        else:
            loglik += -1e300
    return alpha, loglik

def viterbi(
    observations: List[int],
    transition: List[List[float]],
    emission: List[List[float]],
    start: List[float],
) -> List[int]:
    T = len(observations)
    N = len(start)
    log_trans = [[math.log(p + 1e-300) for p in row] for row in transition]
    log_emit = [[math.log(p + 1e-300) for p in row] for row in emission]
    log_start = [math.log(p + 1e-300) for p in start]
    delta = [[-1e300] * N for _ in range(T)]
    psi = [[0] * N for _ in range(T)]
    for j in range(N):
        delta[0][j] = log_start[j] + log_emit[j][observations[0]]
    for t in range(1, T):
        for j in range(N):
            best, arg = -1e300, 0
            for i in range(N):
                val = delta[t - 1][i] + log_trans[i][j]
                if val > best:
                    best, arg = val, i
            delta[t][j] = best + log_emit[j][observations[t]]
            psi[t][j] = arg
    path = [0] * T
    path[-1] = max(range(N), key=lambda j: delta[-1][j])
    for t in range(T - 2, -1, -1):
        path[t] = psi[t + 1][path[t + 1]]
    return path

if __name__ == "__main__":
    trans = [[0.9, 0.1], [0.1, 0.9]]
    emit = [[0.5, 0.5], [0.1, 0.9]]
    start = [0.5, 0.5]
    obs = [0, 1, 1, 1, 1, 1, 1, 0]
    alpha, ll = forward(obs, trans, emit, start)
    assert ll < 0
    path = viterbi(obs, trans, emit, start)
    assert len(path) == len(obs)
    assert all(s in (0, 1) for s in path)
    assert 1 in path[1:7]
    print("hmm self-tests passed")
