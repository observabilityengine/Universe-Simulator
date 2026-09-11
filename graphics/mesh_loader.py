"""Mesh data structure and basic loaders."""
from __future__ import annotations
from typing import List, Tuple

Vec3 = Tuple[float, float, float]


class Mesh:
    def __init__(self):
        self.vertices: List[Vec3] = []
        self.faces: List[Tuple[int, int, int]] = []
        self.normals: List[Vec3] = []

    def add_vertex(self, v: Vec3) -> int:
        self.vertices.append(v)
        return len(self.vertices) - 1

    def add_face(self, i0: int, i1: int, i2: int) -> None:
        self.faces.append((i0, i1, i2))


def make_cube() -> Mesh:
    m = Mesh()
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-1, 1):
                m.add_vertex((float(x), float(y), float(z)))
    # simplified faces
    faces = [(0,1,3),(0,3,2),(4,6,7),(4,7,5),(0,4,5),(0,5,1),(2,3,7),(2,7,6),(0,2,6),(0,6,4),(1,5,7),(1,7,3)]
    for f in faces:
        m.add_face(*f)
    return m


if __name__ == "__main__":
    m = make_cube()
    assert len(m.vertices) == 8
    assert len(m.faces) == 12
    print(f"mesh_loader verts={len(m.vertices)} faces={len(m.faces)}")
    print("mesh_loader self-tests passed")
