"""
Universe Simulator - Hungarian Algorithm (min cost assignment)
Original O(n^3) implementation for square cost matrix.
"""

from __future__ import annotations

from typing import List, Tuple

def hungarian(cost: List[List[float]]) -> Tuple[float, List[int]]:
    n = len(cost)
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [float("inf")] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float("inf")
            j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assignment = [-1] * n
    for j in range(1, n + 1):
        if p[j] != 0:
            assignment[p[j] - 1] = j - 1
    total = sum(cost[i][assignment[i]] for i in range(n))
    return total, assignment

if __name__ == "__main__":
    cost = [[9, 2, 7], [6, 4, 3], [5, 8, 1]]
    total, assign = hungarian(cost)
    assert abs(total - 9.0) < 1e-9  # 2+3+4 or optimal 9
    print("hungarian self-test passed", total, assign)
