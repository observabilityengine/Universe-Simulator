"""Porter-like stemmer (simplified rules)."""
from __future__ import annotations


def stem(word: str) -> str:
    w = word.lower()
    for suffix in ("ational", "tional", "enci", "anci", "izer", "alli", "entli", "eli", "ousli",
                   "ization", "ation", "ator", "alism", "iveness", "fulness", "ousness", "aliti",
                   "iviti", "biliti", "ing", "ed", "ly", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            # simplified: just strip
            if suffix in ("ational", "tional"):
                return w[:-len(suffix)] + ("ate" if suffix == "ational" else "tion")
            if suffix == "ing" and len(w) > 5:
                return w[:-3]
            if suffix == "ed" and len(w) > 4:
                return w[:-2]
            if suffix == "ly" and len(w) > 4:
                return w[:-2]
            if suffix == "es" and len(w) > 4:
                return w[:-2]
            if suffix == "s" and not w.endswith("ss") and len(w) > 3:
                return w[:-1]
            return w[:-len(suffix)]
    return w


if __name__ == "__main__":
    assert stem("running") == "runn" or stem("running").startswith("run")
    assert stem("cats") == "cat"
    print(f"stemming running->{stem('running')} cats->{stem('cats')}")
    print("stemming self-tests passed")
