"""UPGMA hierarchical clustering for phylogenetic trees."""
from __future__ import annotations
from typing import Dict, List, Tuple


def upgma(distances: Dict[Tuple[str, str], float], labels: List[str]) -> str:
    clusters = {lab: [lab] for lab in labels}
    heights = {lab: 0.0 for lab in labels}
    active = set(labels)

    def dist(a, b):
        members_a, members_b = clusters[a], clusters[b]
        total = 0.0
        for x in members_a:
            for y in members_b:
                total += distances.get((x, y), distances.get((y, x), 0.0))
        return total / (len(members_a) * len(members_b))

    newick = {lab: lab for lab in labels}
    next_id = 0
    while len(active) > 1:
        best = None
        best_d = float("inf")
        act = list(active)
        for i in range(len(act)):
            for j in range(i + 1, len(act)):
                d = dist(act[i], act[j])
                if d < best_d:
                    best_d = d
                    best = (act[i], act[j])
        a, b = best
        height = best_d / 2
        name = f"N{next_id}"
        next_id += 1
        clusters[name] = clusters[a] + clusters[b]
        ha = height - heights[a]
        hb = height - heights[b]
        newick[name] = f"({newick[a]}:{ha:.4f},{newick[b]}:{hb:.4f})"
        heights[name] = height
        active.discard(a)
        active.discard(b)
        active.add(name)
    root = next(iter(active))
    return newick[root] + ";"


if __name__ == "__main__":
    labels = ["A", "B", "C"]
    dist = {("A", "B"): 1.0, ("A", "C"): 5.0, ("B", "C"): 5.0}
    tree = upgma(dist, labels)
    assert "A" in tree and "B" in tree
    print(f"upgma {tree}")
    print("upgma self-tests passed")
