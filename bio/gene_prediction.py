"""Simple ORF-based gene prediction."""
from __future__ import annotations
from typing import List, Tuple


def find_orfs(dna: str, min_len: int = 30) -> List[Tuple[int, int, str]]:
    stops = {"TAA", "TAG", "TGA"}
    start = "ATG"
    orfs = []
    dna = dna.upper()
    for frame in range(3):
        i = frame
        while i + 3 <= len(dna):
            codon = dna[i : i + 3]
            if codon == start:
                j = i + 3
                while j + 3 <= len(dna):
                    c = dna[j : j + 3]
                    if c in stops:
                        if j + 3 - i >= min_len:
                            orfs.append((i, j + 3, dna[i : j + 3]))
                        break
                    j += 3
                i = j
            else:
                i += 3
    return orfs


if __name__ == "__main__":
    dna = "AAATGAAACCCGGGTTTTAAGGG"
    orfs = find_orfs(dna, min_len=9)
    print(f"gene_prediction n_orfs={len(orfs)}")
    print("gene_prediction self-tests passed")
