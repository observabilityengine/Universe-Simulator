"""Map of points keyed by geohash prefix."""
from __future__ import annotations
from typing import Dict, List, Tuple
from .geohash import encode


class GeoHashMap:
    def __init__(self, precision: int = 5):
        self.precision = precision
        self.data: Dict[str, List[Tuple[float, float, object]]] = {}

    def insert(self, lat: float, lon: float, value=None) -> None:
        gh = encode(lat, lon, self.precision)
        self.data.setdefault(gh, []).append((lat, lon, value))

    def query(self, lat: float, lon: float) -> List:
        gh = encode(lat, lon, self.precision)
        return self.data.get(gh, [])


if __name__ == "__main__":
    m = GeoHashMap(4)
    m.insert(37.7, -122.4, "SF")
    res = m.query(37.7, -122.4)
    assert len(res) == 1
    print(f"geo_hash_map {res}")
    print("geo_hash_map self-tests passed")
