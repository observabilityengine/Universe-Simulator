"""ASCII STL parser."""
from __future__ import annotations
from .mesh_loader import Mesh


def parse_stl_ascii(text: str) -> Mesh:
    m = Mesh()
    verts_in_facet = []
    for line in text.splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "vertex" and len(parts) >= 4:
            verts_in_facet.append((float(parts[1]), float(parts[2]), float(parts[3])))
            if len(verts_in_facet) == 3:
                i0 = m.add_vertex(verts_in_facet[0])
                i1 = m.add_vertex(verts_in_facet[1])
                i2 = m.add_vertex(verts_in_facet[2])
                m.add_face(i0, i1, i2)
                verts_in_facet = []
    return m


if __name__ == "__main__":
    stl = """solid test
  facet normal 0 0 1
    outer loop
      vertex 0 0 0
      vertex 1 0 0
      vertex 0 1 0
    endloop
  endfacet
endsolid test"""
    m = parse_stl_ascii(stl)
    assert len(m.faces) == 1
    print("stl_parser self-tests passed")
