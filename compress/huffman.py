"""
Module 66 – Huffman Coding
Frequency-based prefix code + encode/decode.
Complete implementation.
"""

from __future__ import annotations
import heapq
from collections import Counter
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass(order=True)
class Node:
    freq: int
    char: Optional[str] = field(compare=False, default=None)
    left: Optional["Node"] = field(compare=False, default=None)
    right: Optional["Node"] = field(compare=False, default=None)


def build_tree(text: str) -> Node:
    freq = Counter(text)
    heap = [Node(f, c) for c, f in freq.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        only = heapq.heappop(heap)
        return Node(only.freq, left=only)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        parent = Node(a.freq + b.freq, left=a, right=b)
        heapq.heappush(heap, parent)
    return heap[0]


def build_codes(node: Node, prefix: str = "", table: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    if table is None:
        table = {}
    if node.char is not None:
        table[node.char] = prefix or "0"
    else:
        if node.left:
            build_codes(node.left, prefix + "0", table)
        if node.right:
            build_codes(node.right, prefix + "1", table)
    return table


def huffman_encode(text: str) -> Tuple[str, Dict[str, str]]:
    if not text:
        return "", {}
    root = build_tree(text)
    codes = build_codes(root)
    encoded = "".join(codes[c] for c in text)
    return encoded, codes


def huffman_decode(encoded: str, codes: Dict[str, str]) -> str:
    rev = {v: k for k, v in codes.items()}
    result = []
    current = ""
    for bit in encoded:
        current += bit
        if current in rev:
            result.append(rev[current])
            current = ""
    return "".join(result)


if __name__ == "__main__":
    print("Testing Huffman Coding...")
    text = "abracadabra"
    encoded, codes = huffman_encode(text)
    decoded = huffman_decode(encoded, codes)
    print(f"  Original: {text}")
    print(f"  Codes: {codes}")
    print(f"  Encoded length: {len(encoded)} bits")
    print(f"  Decoded: {decoded}")
    print(f"  Match: {text == decoded}")
    print("Huffman Coding module OK.")
