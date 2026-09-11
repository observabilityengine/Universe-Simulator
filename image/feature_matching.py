"""Brute-force feature matching with Hamming / L2 distance."""
from __future__ import annotations
from typing import List, Tuple


def hamming(a: List[int], b: List[int]) -> int:
    return sum(x != y for x, y in zip(a, b))


def l2(a: List[float], b: List[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def match_features(
    desc1: List[List],
    desc2: List[List],
    metric: str = "hamming",
    max_dist: float = 10,
) -> List[Tuple[int, int, float]]:
    dist_fn = hamming if metric == "hamming" else l2
    matches = []
    for i, d1 in enumerate(desc1):
        best_j, best_d = -1, float("inf")
        for j, d2 in enumerate(desc2):
            d = dist_fn(d1, d2)
            if d < best_d:
                best_d, best_j = d, j
        if best_j >= 0 and best_d <= max_dist:
            matches.append((i, best_j, float(best_d)))
    return matches


if __name__ == "__main__":
    d1 = [[1, 0, 1, 0], [0, 1, 0, 1]]
    d2 = [[1, 0, 1, 0], [1, 1, 0, 0]]
    m = match_features(d1, d2, max_dist=2)
    assert (0, 0, 0.0) in m or any(p[0] == 0 for p in m)
    print(f"feature_matching {m}")
    print("feature_matching self-tests passed")
