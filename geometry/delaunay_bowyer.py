"""Bowyer-Watson algorithm for Delaunay triangulation in 2D.

Complexity: O(n^2) worst-case (typical for incremental). Original implementation.
"""
from __future__ import annotations

from typing import List, Tuple, Set

Point = Tuple[float, float]
Triangle = Tuple[Point, Point, Point]


def _circumcircle(t: Triangle) -> Tuple[Point, float]:
    """Return (center, radius^2) of the circumcircle of triangle t."""
    (ax, ay), (bx, by), (cx, cy) = t
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-15:
        return ((0.0, 0.0), 1e18)
    ux = (
        (ax**2 + ay**2) * (by - cy)
        + (bx**2 + by**2) * (cy - ay)
        + (cx**2 + cy**2) * (ay - by)
    ) / d
    uy = (
        (ax**2 + ay**2) * (cx - bx)
        + (bx**2 + by**2) * (ax - cx)
        + (cx**2 + cy**2) * (bx - ax)
    ) / d
    r2 = (ux - ax) ** 2 + (uy - ay) ** 2
    return ((ux, uy), r2)


def _in_circumcircle(p: Point, t: Triangle) -> bool:
    center, r2 = _circumcircle(t)
    return (p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2 < r2 - 1e-12


def _edges(t: Triangle) -> List[Tuple[Point, Point]]:
    a, b, c = t
    return [(a, b), (b, c), (c, a)]


def _same_edge(e1: Tuple[Point, Point], e2: Tuple[Point, Point]) -> bool:
    return (e1[0] == e2[0] and e1[1] == e2[1]) or (e1[0] == e2[1] and e1[1] == e2[0])


def delaunay_bowyer(points: List[Point]) -> List[Triangle]:
    """
    Compute the Delaunay triangulation of a set of 2D points
    using the Bowyer-Watson incremental algorithm.
    Returns a list of triangles (each a 3-tuple of points).
    """
    if len(points) < 3:
        return []

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    dx = max_x - min_x or 1.0
    dy = max_y - min_y or 1.0
    delta = max(dx, dy) * 10
    super_tri: Triangle = (
        (min_x - delta, min_y - delta),
        (min_x + 2 * dx + delta, min_y - delta),
        (min_x + dx / 2, max_y + delta),
    )
    triangles: List[Triangle] = [super_tri]

    for p in points:
        bad: List[Triangle] = [t for t in triangles if _in_circumcircle(p, t)]
        boundary: List[Tuple[Point, Point]] = []
        for t in bad:
            for e in _edges(t):
                shared = False
                for other in bad:
                    if other is t:
                        continue
                    for e2 in _edges(other):
                        if _same_edge(e, e2):
                            shared = True
                            break
                    if shared:
                        break
                if not shared:
                    boundary.append(e)
        triangles = [t for t in triangles if t not in bad]
        for e in boundary:
            new_tri = (e[0], e[1], p)
            triangles.append(new_tri)

    super_verts = set(super_tri)
    result = [
        t for t in triangles
        if not any(v in super_verts for v in t)
    ]
    return result


if __name__ == "__main__":
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    tris = delaunay_bowyer(pts)
    assert len(tris) == 2, len(tris)
    used = set()
    for t in tris:
        for v in t:
            used.add(v)
    assert set(pts).issubset(used)
    colinear = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    tris2 = delaunay_bowyer(colinear)
    assert isinstance(tris2, list)
    print("delaunay_bowyer self-tests passed")
