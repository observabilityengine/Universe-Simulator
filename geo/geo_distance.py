"""Unified geo distance dispatcher."""
from __future__ import annotations
from .haversine import haversine
from .vincenty import vincenty_distance


def geo_distance(lat1: float, lon1: float, lat2: float, lon2: float, method: str = "haversine") -> float:
    if method == "vincenty":
        return vincenty_distance(lat1, lon1, lat2, lon2) / 1000.0
    return haversine(lat1, lon1, lat2, lon2)


if __name__ == "__main__":
    d = geo_distance(0, 0, 0, 1)
    assert 100 < d < 120
    print(f"geo_distance={d:.1f} km")
    print("geo_distance self-tests passed")
