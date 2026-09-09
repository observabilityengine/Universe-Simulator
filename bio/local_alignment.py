"""Local alignment wrapper (Smith-Waterman)."""
from __future__ import annotations
from .smith_waterman import smith_waterman


def local_align(a: str, b: str) -> tuple:
    return smith_waterman(a, b)


if __name__ == "__main__":
    s, aa, bb = local_align("ACACACTA", "AGCACACA")
    assert s > 0
    print(f"local_alignment score={s}")
    print("local_alignment self-tests passed")
