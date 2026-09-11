"""Image thresholding – fixed, Otsu-style."""
from __future__ import annotations
from typing import List

Image = List[List[float]]


def threshold(img: Image, t: float = 0.5) -> Image:
    return [[1.0 if v >= t else 0.0 for v in row] for row in img]


def otsu_threshold(img: Image) -> float:
    flat = [v for row in img for v in row]
    n = len(flat)
    if n == 0:
        return 0.5
    hist = [0] * 256
    for v in flat:
        hist[min(255, max(0, int(v * 255)))] += 1
    total_sum = sum(i * hist[i] for i in range(256))
    sum_b, w_b, max_var, thresh = 0.0, 0, 0.0, 0
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = n - w_b
        if w_f == 0:
            break
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (total_sum - sum_b) / w_f
        var = w_b * w_f * (m_b - m_f) ** 2
        if var > max_var:
            max_var, thresh = var, t
    return thresh / 255.0


if __name__ == "__main__":
    img = [[0.1, 0.2], [0.8, 0.9]]
    t = otsu_threshold(img)
    binary = threshold(img, t)
    assert binary[1][1] == 1.0
    print(f"thresholding otsu={t:.2f}")
    print("thresholding self-tests passed")
