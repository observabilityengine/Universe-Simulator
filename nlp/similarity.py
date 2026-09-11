"""Text similarity metrics."""
from __future__ import annotations
from typing import List, Set


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def cosine_bow(a: List[str], b: List[str]) -> float:
    from collections import Counter
    ca, cb = Counter(a), Counter(b)
    keys = set(ca) | set(cb)
    dot = sum(ca[k] * cb[k] for k in keys)
    na = sum(v * v for v in ca.values()) ** 0.5
    nb = sum(v * v for v in cb.values()) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


if __name__ == "__main__":
    assert jaccard({"a", "b"}, {"b", "c"}) == 1 / 3
    assert cosine_bow(["a", "b"], ["a", "b"]) == 1.0
    print("similarity self-tests passed")
