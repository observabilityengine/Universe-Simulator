"""Huffman coding for strings."""
from __future__ import annotations
import heapq
from collections import Counter
from typing import Dict, Optional, Tuple


class Node:
    __slots__ = ("char", "freq", "left", "right")

    def __init__(self, char: Optional[str], freq: int, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "Node") -> bool:
        return self.freq < other.freq


def build_huffman(text: str) -> Tuple[Optional[Node], Dict[str, str]]:
    if not text:
        return None, {}
    freq = Counter(text)
    heap = [Node(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        only = heap[0]
        return only, {only.char: "0"}
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, Node(None, a.freq + b.freq, a, b))
    root = heap[0]
    codes: Dict[str, str] = {}

    def walk(node: Node, path: str) -> None:
        if node.char is not None:
            codes[node.char] = path or "0"
            return
        if node.left:
            walk(node.left, path + "0")
        if node.right:
            walk(node.right, path + "1")

    walk(root, "")
    return root, codes


def huffman_encode(text: str, codes: Dict[str, str]) -> str:
    return "".join(codes[c] for c in text)


def huffman_decode(bits: str, root: Node) -> str:
    if root.char is not None:
        return root.char * len(bits)
    out = []
    node = root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.char is not None:
            out.append(node.char)
            node = root
    return "".join(out)


if __name__ == "__main__":
    text = "this is an example for huffman encoding"
    root, codes = build_huffman(text)
    encoded = huffman_encode(text, codes)
    decoded = huffman_decode(encoded, root)
    assert decoded == text
    print(f"huffman_codes bits={len(encoded)} chars={len(text)}")
    print("huffman_codes self-tests passed")
