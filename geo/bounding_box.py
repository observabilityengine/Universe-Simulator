"""Bounding box utilities."""
from __future__ import annotations
from typing import List, Tuple

BBox = Tuple[float, float, float, float]


def make_bbox(points: List[Tuple[float, float]]) -> BBox:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def intersects(a: BBox, b: BBox) -> bool:
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def contains(bbox: BBox, point: Tuple[float, float]) -> bool:
    return bbox[0] <= point[0] <= bbox[2] and bbox[1] <= point[1] <= bbox[3]


if __name__ == "__main__":
    bb = make_bbox([(0, 0), (1, 2), (3, 1)])
    assert bb == (0, 0, 3, 2)
    assert contains(bb, (1, 1))
    print(f"bounding_box {bb}")
    print("bounding_box self-tests passed")
