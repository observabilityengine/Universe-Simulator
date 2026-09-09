"""Geohash encode/decode."""
from __future__ import annotations
from typing import Tuple

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"


def encode(lat: float, lon: float, precision: int = 8) -> str:
    lat_min, lat_max = -90.0, 90.0
    lon_min, lon_max = -180.0, 180.0
    bits = []
    is_lon = True
    while len(bits) < precision * 5:
        if is_lon:
            mid = (lon_min + lon_max) / 2
            if lon >= mid:
                bits.append(1)
                lon_min = mid
            else:
                bits.append(0)
                lon_max = mid
        else:
            mid = (lat_min + lat_max) / 2
            if lat >= mid:
                bits.append(1)
                lat_min = mid
            else:
                bits.append(0)
                lat_max = mid
        is_lon = not is_lon
    chars = []
    for i in range(0, len(bits), 5):
        idx = 0
        for b in bits[i : i + 5]:
            idx = (idx << 1) | b
        chars.append(BASE32[idx])
    return "".join(chars)


def decode(gh: str) -> Tuple[float, float]:
    bits = []
    for c in gh:
        idx = BASE32.index(c)
        for i in range(4, -1, -1):
            bits.append((idx >> i) & 1)
    lat_min, lat_max = -90.0, 90.0
    lon_min, lon_max = -180.0, 180.0
    is_lon = True
    for b in bits:
        if is_lon:
            mid = (lon_min + lon_max) / 2
            if b:
                lon_min = mid
            else:
                lon_max = mid
        else:
            mid = (lat_min + lat_max) / 2
            if b:
                lat_min = mid
            else:
                lat_max = mid
        is_lon = not is_lon
    return (lat_min + lat_max) / 2, (lon_min + lon_max) / 2


if __name__ == "__main__":
    gh = encode(37.77, -122.42, 6)
    lat, lon = decode(gh)
    assert abs(lat - 37.77) < 0.1 and abs(lon + 122.42) < 0.1
    print(f"geohash {gh} -> {lat:.3f},{lon:.3f}")
    print("geohash self-tests passed")
