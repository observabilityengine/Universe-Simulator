"""Phylogenetic tree utilities – Newick parse and height."""
from __future__ import annotations


def parse_newick_simple(newick: str) -> str:
    return newick.strip().rstrip(";")


def tree_height(newick: str) -> float:
    total = 0.0
    i = 0
    while i < len(newick):
        if newick[i] == ":":
            j = i + 1
            while j < len(newick) and (newick[j].isdigit() or newick[j] in ".eE+-"):
                j += 1
            total += float(newick[i + 1 : j])
            i = j
        else:
            i += 1
    return total


if __name__ == "__main__":
    t = parse_newick_simple("(A:1,B:2);")
    h = tree_height(t)
    assert abs(h - 3) < 1e-6
    print(f"phylogenetic_tree height={h}")
    print("phylogenetic_tree self-tests passed")
