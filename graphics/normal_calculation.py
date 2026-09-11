"""Per-face and per-vertex normal calculation."""
from __future__ import annotations
import math
from typing import List, Tuple
from .mesh_loader import Mesh

Vec3 = Tuple[float, float, float]


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _norm(a: Vec3) -> Vec3:
    l = math.sqrt(a[0]**2+a[1]**2+a[2]**2) or 1.0
    return (a[0]/l, a[1]/l, a[2]/l)


def face_normals(mesh: Mesh) -> List[Vec3]:
    normals = []
    for i0, i1, i2 in mesh.faces:
        v0, v1, v2 = mesh.vertices[i0], mesh.vertices[i1], mesh.vertices[i2]
        e1 = (v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2])
        e2 = (v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2])
        normals.append(_norm(_cross(e1, e2)))
    return normals


def vertex_normals(mesh: Mesh) -> List[Vec3]:
    fn = face_normals(mesh)
    acc = [(0.0, 0.0, 0.0) for _ in mesh.vertices]
    counts = [0] * len(mesh.vertices)
    for fi, (i0, i1, i2) in enumerate(mesh.faces):
        for idx in (i0, i1, i2):
            n = fn[fi]
            a = acc[idx]
            acc[idx] = (a[0]+n[0], a[1]+n[1], a[2]+n[2])
            counts[idx] += 1
    return [_norm(acc[i]) if counts[i] else (0, 0, 1) for i in range(len(acc))]


if __name__ == "__main__":
    from .mesh_loader import make_cube
    m = make_cube()
    fn = face_normals(m)
    assert len(fn) == len(m.faces)
    print(f"normal_calculation face_n={fn[0]}")
    print("normal_calculation self-tests passed")
