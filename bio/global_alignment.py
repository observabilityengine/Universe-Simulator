"""Global alignment wrapper (Needleman-Wunsch)."""
from __future__ import annotations
from .needleman_wunsch import needleman_wunsch


def global_align(a: str, b: str) -> tuple:
    return needleman_wunsch(a, b)


if __name__ == "__main__":
    s, aa, bb = global_align("ACGT", "AGT")
    assert len(aa) == len(bb)
    print(f"global_alignment {aa} / {bb}")
    print("global_alignment self-tests passed")
