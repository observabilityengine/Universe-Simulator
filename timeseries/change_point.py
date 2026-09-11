"""Binary segmentation change-point detection."""
from __future__ import annotations
from typing import List


def _cost(series: List[float], start: int, end: int) -> float:
    seg = series[start:end]
    if not seg:
        return 0.0
    mean = sum(seg) / len(seg)
    return sum((x - mean) ** 2 for x in seg)


def find_change_points(series: List[float], max_cp: int = 2, min_size: int = 3) -> List[int]:
    n = len(series)
    cps = []
    segments = [(0, n)]
    for _ in range(max_cp):
        best_gain, best_cp, best_seg = 0.0, None, None
        for s, e in segments:
            if e - s < 2 * min_size:
                continue
            base = _cost(series, s, e)
            for c in range(s + min_size, e - min_size + 1):
                gain = base - _cost(series, s, c) - _cost(series, c, e)
                if gain > best_gain:
                    best_gain, best_cp, best_seg = gain, c, (s, e)
        if best_cp is None:
            break
        cps.append(best_cp)
        segments.remove(best_seg)
        segments.append((best_seg[0], best_cp))
        segments.append((best_cp, best_seg[1]))
    return sorted(cps)


if __name__ == "__main__":
    s = [0.0] * 20 + [5.0] * 20
    cps = find_change_points(s, max_cp=1)
    assert any(abs(c - 20) < 3 for c in cps)
    print(f"change_point {cps}")
    print("change_point self-tests passed")
