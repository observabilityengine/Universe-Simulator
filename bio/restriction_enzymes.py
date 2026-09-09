"""Restriction enzyme site finder."""
from __future__ import annotations
from typing import Dict, List

COMMON_ENZYMES: Dict[str, str] = {
    "EcoRI": "GAATTC",
    "BamHI": "GGATCC",
    "HindIII": "AAGCTT",
    "NotI": "GCGGCCGC",
    "XhoI": "CTCGAG",
}


def find_sites(dna: str, enzyme: str = "EcoRI") -> List[int]:
    pattern = COMMON_ENZYMES.get(enzyme, enzyme)
    dna = dna.upper()
    sites = []
    for i in range(len(dna) - len(pattern) + 1):
        if dna[i : i + len(pattern)] == pattern:
            sites.append(i)
    return sites


def digest(dna: str, enzyme: str = "EcoRI") -> List[str]:
    sites = find_sites(dna, enzyme)
    if not sites:
        return [dna]
    pattern = COMMON_ENZYMES.get(enzyme, enzyme)
    fragments = []
    prev = 0
    for s in sites:
        fragments.append(dna[prev : s + len(pattern) // 2])
        prev = s + len(pattern) // 2
    fragments.append(dna[prev:])
    return fragments


if __name__ == "__main__":
    dna = "AAAGAATTCAAA"
    sites = find_sites(dna, "EcoRI")
    assert 3 in sites
    print(f"restriction_enzymes sites={sites}")
    print("restriction_enzymes self-tests passed")
