"""Codon usage table and RSCU calculation."""
from __future__ import annotations
from typing import Dict


def codon_counts(dna: str) -> Dict[str, int]:
    dna = dna.upper()
    counts: Dict[str, int] = {}
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i : i + 3]
        if len(codon) == 3:
            counts[codon] = counts.get(codon, 0) + 1
    return counts


def rscu(counts: Dict[str, int], amino_map: Dict[str, str]) -> Dict[str, float]:
    aa_totals: Dict[str, int] = {}
    aa_ncodons: Dict[str, int] = {}
    for codon, aa in amino_map.items():
        aa_ncodons[aa] = aa_ncodons.get(aa, 0) + 1
        aa_totals[aa] = aa_totals.get(aa, 0) + counts.get(codon, 0)
    result = {}
    for codon, aa in amino_map.items():
        expected = aa_totals[aa] / max(aa_ncodons[aa], 1)
        result[codon] = counts.get(codon, 0) / expected if expected > 0 else 0.0
    return result


if __name__ == "__main__":
    counts = codon_counts("ATGATGAAATTT")
    assert counts.get("ATG", 0) == 2
    print(f"codon_usage {counts}")
    print("codon_usage self-tests passed")
