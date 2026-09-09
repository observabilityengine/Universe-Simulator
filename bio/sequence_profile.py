"""Position-specific scoring matrix / sequence profile from alignment."""
from __future__ import annotations
from typing import Dict, List


def build_profile(aligned: List[str], pseudocount: float = 0.25) -> List[Dict[str, float]]:
    if not aligned:
        return []
    L = len(aligned[0])
    alphabet = "ACGT"
    profile = []
    for i in range(L):
        counts = {b: pseudocount for b in alphabet}
        for seq in aligned:
            if seq[i] in counts:
                counts[seq[i]] += 1
        total = sum(counts.values())
        profile.append({b: counts[b] / total for b in alphabet})
    return profile


if __name__ == "__main__":
    aln = ["ACGT", "AGGT", "ACGA"]
    prof = build_profile(aln)
    assert abs(sum(prof[0].values()) - 1) < 1e-6
    assert prof[1]["G"] > prof[1]["C"]
    print(f"sequence_profile col0={prof[0]}")
    print("sequence_profile self-tests passed")
