"""Haversine great-circle distance."""
from __future__ import annotations
import math

R_EARTH_KM = 6371.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    rlat1, rlon1, rlat2, rlon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1
    a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
    return 2 * R_EARTH_KM * math.asin(math.sqrt(a))


if __name__ == "__main__":
    d = haversine(40.71, -74.01, 34.05, -118.24)
    assert 3900 < d < 4000
    print(f"haversine NYC-LA={d:.0f} km")
    print("haversine self-tests passed")
