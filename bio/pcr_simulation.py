"""PCR amplification simulation."""
from __future__ import annotations
from typing import Tuple


def pcr_cycles(template_copies: float, efficiency: float = 0.95, cycles: int = 30) -> float:
    return template_copies * ((1 + efficiency) ** cycles)


def primer_anneal(template: str, primer: str) -> bool:
    return primer.upper() in template.upper()


def amplify(template: str, fwd: str, rev: str, cycles: int = 25) -> Tuple[float, str]:
    if not primer_anneal(template, fwd):
        return 0.0, ""
    product = template
    copies = pcr_cycles(1.0, 0.9, cycles)
    return copies, product


if __name__ == "__main__":
    c = pcr_cycles(1, 1.0, 10)
    assert abs(c - 1024) < 1e-6
    print(f"pcr_simulation copies_10={c}")
    print("pcr_simulation self-tests passed")
