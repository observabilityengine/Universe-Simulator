"""English stopword list and filter."""
from __future__ import annotations
from typing import List, Set

STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may", "might",
    "must", "shall", "can", "need", "dare", "ought", "used", "it", "its", "this",
    "that", "these", "those", "i", "you", "he", "she", "we", "they", "me", "him",
    "her", "us", "them", "my", "your", "his", "our", "their", "what", "which",
    "who", "whom", "whose", "where", "when", "why", "how", "all", "each", "every",
    "both", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "just", "about",
}


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t.lower() not in STOPWORDS]


if __name__ == "__main__":
    toks = ["the", "quick", "brown", "fox"]
    filtered = remove_stopwords(toks)
    assert "the" not in filtered and "quick" in filtered
    print(f"stopwords {filtered}")
    print("stopwords self-tests passed")
