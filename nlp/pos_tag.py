"""Simple rule-based POS tagger."""
from __future__ import annotations
from typing import List, Tuple

TAGS = {
    "the": "DET", "a": "DET", "an": "DET", "this": "DET", "that": "DET",
    "is": "VERB", "are": "VERB", "was": "VERB", "were": "VERB", "be": "VERB",
    "have": "VERB", "has": "VERB", "do": "VERB", "does": "VERB",
    "and": "CONJ", "or": "CONJ", "but": "CONJ",
    "in": "ADP", "on": "ADP", "at": "ADP", "to": "ADP", "for": "ADP", "of": "ADP",
    "i": "PRON", "you": "PRON", "he": "PRON", "she": "PRON", "it": "PRON", "we": "PRON", "they": "PRON",
}


def pos_tag(tokens: List[str]) -> List[Tuple[str, str]]:
    result = []
    for t in tokens:
        low = t.lower()
        if low in TAGS:
            result.append((t, TAGS[low]))
        elif t[0].isupper() and len(t) > 1:
            result.append((t, "PROPN"))
        elif t.endswith("ly"):
            result.append((t, "ADV"))
        elif t.endswith(("ing", "ed", "s")) and len(t) > 4:
            result.append((t, "VERB"))
        else:
            result.append((t, "NOUN"))
    return result


if __name__ == "__main__":
    tags = pos_tag(["The", "cat", "sits", "quickly"])
    assert tags[0][1] == "DET"
    assert tags[1][1] == "NOUN"
    print(f"pos_tag {tags}")
    print("pos_tag self-tests passed")
