"""Lexicon-based sentiment analysis."""
from __future__ import annotations
from typing import List

POS = {"good", "great", "excellent", "love", "happy", "best", "wonderful", "amazing", "positive", "nice"}
NEG = {"bad", "terrible", "hate", "awful", "worst", "poor", "negative", "horrible", "sad", "angry"}


def sentiment_score(tokens: List[str]) -> float:
    pos = sum(1 for t in tokens if t.lower() in POS)
    neg = sum(1 for t in tokens if t.lower() in NEG)
    total = pos + neg
    if total == 0:
        return 0.0
    return (pos - neg) / total


def classify_sentiment(text: str) -> str:
    from .tokenize import tokenize
    score = sentiment_score(tokenize(text))
    if score > 0.1:
        return "positive"
    if score < -0.1:
        return "negative"
    return "neutral"


if __name__ == "__main__":
    assert classify_sentiment("this is great and wonderful") == "positive"
    assert classify_sentiment("this is terrible and awful") == "negative"
    print("sentiment self-tests passed")
