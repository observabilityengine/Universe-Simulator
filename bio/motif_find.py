"""Find sequence motifs via k-mer enumeration and PWM scoring."""
from __future__ import annotations
from typing import Dict, List, Tuple


def find_motifs(sequences: List[str], k: int = 4) -> List[Tuple[str, int]]:
    counts: Dict[str, int] = {}
    for seq in sequences:
        for i in range(len(seq) - k + 1):
            mer = seq[i : i + k]
            counts[mer] = counts.get(mer, 0) + 1
    return sorted(counts.items(), key=lambda x: -x[1])


def pwm_score(seq: str, pwm: List[Dict[str, float]]) -> float:
    score = 0.0
    for i, col in enumerate(pwm):
        if i >= len(seq):
            break
        score += col.get(seq[i], -10.0)
    return score


if __name__ == "__main__":
    seqs = ["ACGTACGT", "ACGTAAGG", "ACGTACGA"]
    motifs = find_motifs(seqs, 4)
    assert motifs[0][0].startswith("ACGT")
    print(f"motif_find top={motifs[0]}")
    print("motif_find self-tests passed")
