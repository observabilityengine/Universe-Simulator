"""Image crop."""
from __future__ import annotations
from typing import List

Image = List[List[float]]


def crop(img: Image, y0: int, x0: int, y1: int, x1: int) -> Image:
    return [row[x0:x1] for row in img[y0:y1]]


if __name__ == "__main__":
    img = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    c = crop(img, 0, 1, 2, 3)
    assert c == [[2, 3], [5, 6]]
    print("crop self-tests passed")
