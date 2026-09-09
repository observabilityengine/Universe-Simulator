"""WGS84 ellipsoid constants and ECEF conversion."""
from __future__ import annotations
import math
from typing import Tuple

A = 6378137.0
F = 1 / 298.257223563
E2 = F * (2 - F)


def latlon_to_ecef(lat: float, lon: float, h: float = 0.0) -> Tuple[float, float, float]:
    lat_r, lon_r = math.radians(lat), math.radians(lon)
    N = A / math.sqrt(1 - E2 * math.sin(lat_r) ** 2)
    x = (N + h) * math.cos(lat_r) * math.cos(lon_r)
    y = (N + h) * math.cos(lat_r) * math.sin(lon_r)
    z = (N * (1 - E2) + h) * math.sin(lat_r)
    return x, y, z


if __name__ == "__main__":
    x, y, z = latlon_to_ecef(0, 0)
    assert abs(x - A) < 1
    print(f"wgs84 ECEF equator={x:.0f}")
    print("wgs84 self-tests passed")
