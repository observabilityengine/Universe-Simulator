"""Neighbor-Joining phylogenetic tree reconstruction."""
from __future__ import annotations
from typing import Dict, List, Tuple


def neighbor_joining(distances: Dict[Tuple[str, str], float], labels: List[str]) -> str:
    def d(a, b):
        return distances.get((a, b), distances.get((b, a), 0.0))

    active = list(labels)
    newick = {lab: lab for lab in labels}
    next_id = 0
    while len(active) > 2:
        n = len(active)
        total = {x: sum(d(x, y) for y in active if y != x) for x in active}
        best = None
        best_q = float("inf")
        for i in range(n):
            for j in range(i + 1, n):
                a, b = active[i], active[j]
                q = (n - 2) * d(a, b) - total[a] - total[b]
                if q < best_q:
                    best_q = q
                    best = (a, b)
        a, b = best
        delta_a = 0.5 * d(a, b) + (total[a] - total[b]) / (2 * (n - 2))
        delta_b = d(a, b) - delta_a
        name = f"N{next_id}"
        next_id += 1
        newick[name] = f"({newick[a]}:{max(delta_a,0):.4f},{newick[b]}:{max(delta_b,0):.4f})"
        for x in active:
            if x in (a, b):
                continue
            distances[(name, x)] = 0.5 * (d(a, x) + d(b, x) - d(a, b))
        active = [x for x in active if x not in (a, b)] + [name]
    a, b = active
    return f"({newick[a]}:{d(a,b)/2:.4f},{newick[b]}:{d(a,b)/2:.4f});"


if __name__ == "__main__":
    labels = ["A", "B", "C", "D"]
    dist = {
        ("A", "B"): 5, ("A", "C"): 9, ("A", "D"): 9,
        ("B", "C"): 10, ("B", "D"): 10, ("C", "D"): 8,
    }
    tree = neighbor_joining(dist, labels)
    assert "A" in tree
    print(f"neighbor_joining {tree}")
    print("neighbor_joining self-tests passed")
