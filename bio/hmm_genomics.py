"""Profile HMM for sequence family (Match states – simplified Viterbi)."""
from __future__ import annotations
from typing import List


def viterbi_path(seq: str, match_emit: List[dict], trans: dict) -> List[str]:
    n = len(seq)
    m = len(match_emit)
    dp = [[float("-inf")] * m for _ in range(n)]
    for j in range(m):
        dp[0][j] = match_emit[j].get(seq[0], -10)
    for i in range(1, n):
        for j in range(m):
            emit = match_emit[j].get(seq[i], -10)
            best = max(dp[i - 1][k] + trans.get((k, j), -1) for k in range(m))
            dp[i][j] = best + emit
    path = []
    j = max(range(m), key=lambda x: dp[n - 1][x])
    path.append(f"M{j}")
    for i in range(n - 2, -1, -1):
        best_k, best_v = 0, float("-inf")
        for k in range(m):
            v = dp[i][k] + trans.get((k, j), -1)
            if v > best_v:
                best_v, best_k = v, k
        j = best_k
        path.append(f"M{j}")
    path.reverse()
    return path


if __name__ == "__main__":
    emit = [{"A": 0, "C": -5, "G": -5, "T": -5}, {"A": -5, "C": 0, "G": -5, "T": -5}]
    trans = {(0, 0): -1, (0, 1): 0, (1, 0): -1, (1, 1): 0}
    path = viterbi_path("AC", emit, trans)
    assert len(path) == 2
    print(f"hmm_genomics path={path}")
    print("hmm_genomics self-tests passed")
