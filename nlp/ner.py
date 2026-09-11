"""Simple rule-based named entity recognition."""
from __future__ import annotations
from typing import List, Tuple


def ner_tag(tokens: List[str]) -> List[Tuple[str, str]]:
    result = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t[0].isupper() and i > 0:
            # capitalize after start -> possible entity
            entity = [t]
            j = i + 1
            while j < len(tokens) and tokens[j][0].isupper():
                entity.append(tokens[j])
                j += 1
            result.append((" ".join(entity), "ENTITY"))
            i = j
        else:
            result.append((t, "O"))
            i += 1
    return result


if __name__ == "__main__":
    tags = ner_tag(["I", "met", "John", "Smith", "in", "Paris"])
    entities = [t for t, l in tags if l == "ENTITY"]
    assert any("John" in e for e in entities)
    print(f"ner {tags}")
    print("ner self-tests passed")
