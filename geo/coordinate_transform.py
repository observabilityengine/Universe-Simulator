"""Simple coordinate transforms (deg/rad, local ENU offset)."""
from __future__ import annotations
import math
from typing import Tuple


def deg2rad(d: float) -> float:
    return d * math.pi / 180


def rad2deg(r: float) -> float:
    return r * 180 / math.pi


def enu_offset(lat0: float, lon0: float, lat: float, lon: float) -> Tuple[float, float]:
    R = 6371000
    dlat = deg2rad(lat - lat0)
    dlon = deg2rad(lon - lon0)
    e = dlon * math.cos(deg2rad(lat0)) * R
    n = dlat * R
    return e, n


if __name__ == "__main__":
    e, n = enu_offset(0, 0, 0, 0.001)
    assert abs(e) > 0
    print(f"coordinate_transform e={e:.1f} n={n:.1f}")
    print("coordinate_transform self-tests passed")
