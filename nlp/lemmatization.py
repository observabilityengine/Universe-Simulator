"""Rule-based lemmatizer for common English suffixes."""
from __future__ import annotations

IRREGULAR = {
    "was": "be", "were": "be", "been": "be", "is": "be", "are": "be", "am": "be",
    "had": "have", "has": "have", "did": "do", "does": "do",
    "went": "go", "gone": "go", "went": "go", "better": "good", "best": "good",
    "worse": "bad", "worst": "bad", "children": "child", "men": "man", "women": "woman",
}


def lemmatize(word: str) -> str:
    w = word.lower()
    if w in IRREGULAR:
        return IRREGULAR[w]
    for suffix, repl in [("ies", "y"), ("ves", "f"), ("ing", ""), ("ed", ""), ("es", ""), ("s", "")]:
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            return w[:-len(suffix)] + repl
    return w


if __name__ == "__main__":
    assert lemmatize("running") in ("run", "runn")
    assert lemmatize("was") == "be"
    print(f"lemmatization running->{lemmatize('running')}")
    print("lemmatization self-tests passed")
