"""Nested-loop spatial join on bounding boxes."""
from __future__ import annotations
from typing import List, Tuple

BBox = Tuple[float, float, float, float]


def bbox_intersect(a: BBox, b: BBox) -> bool:
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def spatial_join(left: List[Tuple[int, BBox]], right: List[Tuple[int, BBox]]) -> List[Tuple[int, int]]:
    pairs = []
    for i, bb_a in left:
        for j, bb_b in right:
            if bbox_intersect(bb_a, bb_b):
                pairs.append((i, j))
    return pairs


if __name__ == "__main__":
    L = [(0, (0, 0, 2, 2)), (1, (5, 5, 6, 6))]
    R = [(10, (1, 1, 3, 3)), (11, (10, 10, 11, 11))]
    pairs = spatial_join(L, R)
    assert (0, 10) in pairs
    print(f"spatial_join {pairs}")
    print("spatial_join self-tests passed")
