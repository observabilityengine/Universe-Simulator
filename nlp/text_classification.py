"""Naive Bayes text classifier."""
from __future__ import annotations
import math
from collections import defaultdict
from typing import Dict, List, Tuple


class NaiveBayesClassifier:
    def __init__(self):
        self.class_counts: Dict[str, int] = defaultdict(int)
        self.word_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.vocab: set = set()
        self.n_docs = 0

    def fit(self, documents: List[List[str]], labels: List[str]) -> None:
        for doc, label in zip(documents, labels):
            self.class_counts[label] += 1
            self.n_docs += 1
            for w in doc:
                self.word_counts[label][w] += 1
                self.vocab.add(w)

    def predict(self, doc: List[str]) -> str:
        best_label, best_score = None, float("-inf")
        for label, count in self.class_counts.items():
            log_prior = math.log(count / self.n_docs)
            total_words = sum(self.word_counts[label].values())
            log_lik = 0.0
            for w in doc:
                wc = self.word_counts[label].get(w, 0) + 1
                log_lik += math.log(wc / (total_words + len(self.vocab)))
            score = log_prior + log_lik
            if score > best_score:
                best_score, best_label = score, label
        return best_label or "unknown"


if __name__ == "__main__":
    docs = [["good", "movie"], ["bad", "film"], ["great", "movie"], ["terrible", "film"]]
    labels = ["pos", "neg", "pos", "neg"]
    clf = NaiveBayesClassifier()
    clf.fit(docs, labels)
    assert clf.predict(["good", "great"]) == "pos"
    print("text_classification self-tests passed")
