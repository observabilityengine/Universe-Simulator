"""TF-IDF vectorizer."""
from __future__ import annotations
import math
from typing import Dict, List


def compute_tfidf(documents: List[List[str]]) -> List[Dict[str, float]]:
    n = len(documents)
    df: Dict[str, int] = {}
    for doc in documents:
        for t in set(doc):
            df[t] = df.get(t, 0) + 1
    results = []
    for doc in documents:
        tf: Dict[str, int] = {}
        for t in doc:
            tf[t] = tf.get(t, 0) + 1
        length = len(doc) or 1
        vec = {}
        for t, c in tf.items():
            idf = math.log((n + 1) / (df[t] + 1)) + 1
            vec[t] = (c / length) * idf
        results.append(vec)
    return results


if __name__ == "__main__":
    docs = [["the", "cat", "sat"], ["the", "dog", "sat"], ["cat", "and", "dog"]]
    vecs = compute_tfidf(docs)
    assert "cat" in vecs[0]
    print(f"tfidf doc0={vecs[0]}")
    print("tfidf self-tests passed")
