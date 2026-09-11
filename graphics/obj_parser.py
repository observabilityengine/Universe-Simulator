"""Wavefront OBJ parser (vertices and faces)."""
from __future__ import annotations
from typing import List, Tuple
from .mesh_loader import Mesh


def parse_obj(text: str) -> Mesh:
    m = Mesh()
    for line in text.splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "v" and len(parts) >= 4:
            m.add_vertex((float(parts[1]), float(parts[2]), float(parts[3])))
        elif parts[0] == "f" and len(parts) >= 4:
            idxs = []
            for p in parts[1:4]:
                idxs.append(int(p.split("/")[0]) - 1)
            m.add_face(idxs[0], idxs[1], idxs[2])
    return m


if __name__ == "__main__":
    obj = "v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n"
    m = parse_obj(obj)
    assert len(m.vertices) == 3 and len(m.faces) == 1
    print("obj_parser self-tests passed")
