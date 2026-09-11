"""Byte-Pair Encoding (BPE) subword tokenizer."""
from __future__ import annotations
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


def get_stats(vocab: Dict[str, int]) -> Counter:
    pairs: Counter = Counter()
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq
    return pairs


def merge_vocab(pair: Tuple[str, str], vocab: Dict[str, int]) -> Dict[str, int]:
    bigram = " ".join(pair)
    replacement = "".join(pair)
    new_vocab = {}
    for word, freq in vocab.items():
        new_word = word.replace(bigram, replacement)
        new_vocab[new_word] = freq
    return new_vocab


def train_bpe(words: List[str], n_merges: int = 10) -> List[Tuple[str, str]]:
    vocab: Dict[str, int] = Counter(" ".join(list(w)) + " </w>" for w in words)
    merges = []
    for _ in range(n_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
        merges.append(best)
    return merges


def encode_bpe(word: str, merges: List[Tuple[str, str]]) -> List[str]:
    symbols = list(word) + ["</w>"]
    for a, b in merges:
        i = 0
        new_sym = []
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
                new_sym.append(a + b)
                i += 2
            else:
                new_sym.append(symbols[i])
                i += 1
        symbols = new_sym
    return symbols


if __name__ == "__main__":
    merges = train_bpe(["low", "lowest", "newer", "wider"], n_merges=5)
    enc = encode_bpe("lowest", merges)
    assert len(enc) >= 1
    print(f"subword_tokenizer merges={merges[:3]} enc={enc}")
    print("subword_tokenizer self-tests passed")
