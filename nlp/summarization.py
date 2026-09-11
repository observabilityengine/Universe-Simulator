"""Extractive summarization via sentence scoring."""
from __future__ import annotations
from typing import List
from .tokenize import sent_tokenize, tokenize
from .stopwords import remove_stopwords


def summarize(text: str, n_sentences: int = 2) -> str:
    sents = sent_tokenize(text)
    if len(sents) <= n_sentences:
        return text
    # score by word frequency
    all_tokens = []
    sent_tokens = []
    for s in sents:
        toks = remove_stopwords(tokenize(s))
        sent_tokens.append(toks)
        all_tokens.extend(toks)
    freq: dict = {}
    for t in all_tokens:
        freq[t] = freq.get(t, 0) + 1
    scores = []
    for i, toks in enumerate(sent_tokens):
        score = sum(freq.get(t, 0) for t in toks) / max(len(toks), 1)
        scores.append((score, i))
    top = sorted(scores, reverse=True)[:n_sentences]
    indices = sorted(i for _, i in top)
    return " ".join(sents[i] for i in indices)


if __name__ == "__main__":
    text = "Python is a language. It is popular. Many people use Python. It is easy."
    s = summarize(text, 2)
    assert "Python" in s
    print(f"summarization {s}")
    print("summarization self-tests passed")
