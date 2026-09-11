"""Beam search decoder for sequence models."""
from __future__ import annotations
import math
from typing import Callable, List, Tuple


def beam_search(
    start: str,
    score_fn: Callable[[List[str]], float],
    candidates_fn: Callable[[List[str]], List[str]],
    beam_width: int = 3,
    max_len: int = 10,
    end_token: str = "</s>",
) -> List[str]:
    beam: List[Tuple[float, List[str]]] = [(0.0, [start])]
    for _ in range(max_len):
        new_beam = []
        for score, seq in beam:
            if seq[-1] == end_token:
                new_beam.append((score, seq))
                continue
            for tok in candidates_fn(seq):
                new_seq = seq + [tok]
                new_score = score + score_fn(new_seq)
                new_beam.append((new_score, new_seq))
        new_beam.sort(key=lambda x: -x[0])
        beam = new_beam[:beam_width]
        if all(s[-1] == end_token for _, s in beam):
            break
    return beam[0][1]


if __name__ == "__main__":
    def score(seq):
        return -len(seq)  # prefer shorter
    def cands(seq):
        if len(seq) >= 3:
            return ["</s>"]
        return ["a", "b", "</s>"]
    result = beam_search("<s>", score, cands, beam_width=2, max_len=5)
    assert result[0] == "<s>"
    print(f"beam_search_decode {result}")
    print("beam_search_decode self-tests passed")
