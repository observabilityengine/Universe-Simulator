"""Vincenty inverse formula for geodesic distance on WGS84 ellipsoid."""
from __future__ import annotations
import math

A = 6378137.0
F = 1 / 298.257223563
B = A * (1 - F)


def vincenty_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    L = math.radians(lon2 - lon1)
    U1 = math.atan((1 - F) * math.tan(phi1))
    U2 = math.atan((1 - F) * math.tan(phi2))
    sinU1, cosU1 = math.sin(U1), math.cos(U1)
    sinU2, cosU2 = math.sin(U2), math.cos(U2)
    lam = L
    for _ in range(100):
        sinLam, cosLam = math.sin(lam), math.cos(lam)
        sinSigma = math.sqrt((cosU2 * sinLam) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLam) ** 2)
        if sinSigma == 0:
            return 0.0
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLam
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLam / sinSigma
        cos2Alpha = 1 - sinAlpha ** 2
        cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cos2Alpha if cos2Alpha else 0
        C = F / 16 * cos2Alpha * (4 + F * (4 - 3 * cos2Alpha))
        lam_prev = lam
        lam = L + (1 - C) * F * sinAlpha * (sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM ** 2)))
        if abs(lam - lam_prev) < 1e-12:
            break
    u2 = cos2Alpha * (A ** 2 - B ** 2) / (B ** 2)
    A_ = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B_ = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    dSigma = B_ * sinSigma * (cos2SigmaM + B_ / 4 * (cosSigma * (-1 + 2 * cos2SigmaM ** 2) - B_ / 6 * cos2SigmaM * (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
    return B * A_ * (sigma - dSigma)


if __name__ == "__main__":
    d = vincenty_distance(40.71, -74.01, 34.05, -118.24)
    assert 3900_000 < d < 4000_000
    print(f"vincenty NYC-LA={d/1000:.0f} km")
    print("vincenty self-tests passed")
