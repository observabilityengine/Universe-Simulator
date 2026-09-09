"""Simplified UTM zone and conversion (equatorial approximation)."""
from __future__ import annotations
import math
from typing import Tuple


def utm_zone(lon: float) -> int:
    return int((lon + 180) / 6) + 1


def latlon_to_utm_approx(lat: float, lon: float) -> Tuple[float, float, int]:
    zone = utm_zone(lon)
    lon0 = (zone - 1) * 6 - 180 + 3
    lat_r, lon_r = math.radians(lat), math.radians(lon - lon0)
    x = lon_r * math.cos(lat_r) * 6378137
    y = lat_r * 6378137
    return x + 500000, y, zone


if __name__ == "__main__":
    z = utm_zone(-122.4)
    assert z == 10
    x, y, zone = latlon_to_utm_approx(37.7, -122.4)
    print(f"utm zone={zone} x={x:.0f} y={y:.0f}")
    print("utm self-tests passed")
