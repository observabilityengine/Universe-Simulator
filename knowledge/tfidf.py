"""
Universe Simulator - TF-IDF Vectorizer
Original pure-Python TF-IDF.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Dict, List


class TfidfVectorizer:
    def __init__(self) -> None:
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def fit(self, documents: List[str]) -> None:
        df: Counter = Counter()
        for doc in documents:
            tokens = set(doc.lower().split())
            for t in tokens:
                df[t] += 1
        n = len(documents)
        self.vocab = {t: i for i, t in enumerate(sorted(df))}
        self.idf = {t: math.log((n + 1) / (df[t] + 1)) + 1 for t in df}

    def transform(self, doc: str) -> List[float]:
        tokens = doc.lower().split()
        tf = Counter(tokens)
        vec = [0.0] * len(self.vocab)
        length = len(tokens) or 1
        for t, cnt in tf.items():
            if t in self.vocab:
                vec[self.vocab[t]] = (cnt / length) * self.idf[t]
        return vec


if __name__ == "__main__":
    docs = ["the cat sat", "the dog ran", "cat and dog"]
    v = TfidfVectorizer()
    v.fit(docs)
    vec = v.transform("cat dog")
    assert len(vec) == len(v.vocab)
    assert sum(vec) > 0
    print("tfidf self-test passed", vec)
