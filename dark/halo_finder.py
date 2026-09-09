"""Friends-of-Friends and spherical-overdensity halo finder."""
from __future__ import annotations
import math
from typing import Dict, List, Tuple

Vec = List[float]


def friends_of_friends(positions: List[Vec], linking_length: float) -> List[List[int]]:
    n = len(positions)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    ll2 = linking_length ** 2
    for i in range(n):
        for j in range(i + 1, n):
            d2 = sum((positions[i][d] - positions[j][d]) ** 2 for d in range(len(positions[0])))
            if d2 <= ll2:
                union(i, j)
    groups: Dict[int, List[int]] = {}
    for i in range(n):
        r = find(i)
        groups.setdefault(r, []).append(i)
    return [g for g in groups.values() if len(g) >= 2]


def spherical_overdensity(positions: List[Vec], masses: List[float], center: Vec, rho_crit: float, delta: float = 200.0) -> Tuple[float, float]:
    radii = sorted(
        (math.sqrt(sum((positions[i][d] - center[d]) ** 2 for d in range(len(center)))), i)
        for i in range(len(positions))
    )
    m_enc = 0.0
    r_vir, m_vir = 0.0, 0.0
    for r, i in radii:
        m_enc += masses[i]
        if r < 1e-12:
            continue
        vol = 4.0 / 3.0 * math.pi * r ** 3
        rho = m_enc / vol
        if rho < delta * rho_crit:
            break
        r_vir, m_vir = r, m_enc
    return r_vir, m_vir


if __name__ == "__main__":
    pos = [[0, 0], [0.1, 0], [0.05, 0.05], [5, 5], [5.1, 5]]
    groups = friends_of_friends(pos, 0.2)
    assert len(groups) >= 1
    assert max(len(g) for g in groups) >= 2
    print(f"halo_finder n_groups={len(groups)}")
    print("halo_finder self-tests passed")
