"""
Module 44 – Merkle Tree
Binary Merkle tree for data integrity verification.
Original implementation.
"""

from __future__ import annotations
import hashlib
from typing import List, Tuple, Any


def _leaf_hash(data: Any) -> str:
    return hashlib.sha256(str(data).encode()).hexdigest()


def _node_hash(left: str, right: str) -> str:
    return hashlib.sha256((left + right).encode()).hexdigest()


class MerkleTree:
    def __init__(self, items: List[Any]):
        if not items:
            raise ValueError("Need at least one item")
        self.leaves = [_leaf_hash(x) for x in items]
        self.layers: List[List[str]] = [self.leaves]
        self._build()

    def _build(self) -> None:
        current = self.leaves
        while len(current) > 1:
            next_layer = []
            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1] if i + 1 < len(current) else left
                next_layer.append(_node_hash(left, right))
            self.layers.append(next_layer)
            current = next_layer

    @property
    def root(self) -> str:
        return self.layers[-1][0]

    def proof(self, index: int) -> List[Tuple[str, str]]:
        if index < 0 or index >= len(self.leaves):
            raise IndexError("Index out of range")
        proof = []
        for layer in self.layers[:-1]:
            sibling = index ^ 1
            if sibling < len(layer):
                side = "left" if sibling < index else "right"
                proof.append((layer[sibling], side))
            index //= 2
        return proof

    @staticmethod
    def verify(leaf_data: Any, proof: List[Tuple[str, str]], root: str) -> bool:
        current = _leaf_hash(leaf_data)
        for sibling, side in proof:
            if side == "left":
                current = _node_hash(sibling, current)
            else:
                current = _node_hash(current, sibling)
        return current == root


if __name__ == "__main__":
    print("Testing Merkle Tree...")
    items = ["a", "b", "c", "d", "e"]
    tree = MerkleTree(items)
    print(f"  Root: {tree.root[:16]}...")
    proof = tree.proof(2)
    print(f"  Proof length for index 2: {len(proof)}")
    print(f"  Verify 'c': {MerkleTree.verify('c', proof, tree.root)}")
    print(f"  Verify 'x': {MerkleTree.verify('x', proof, tree.root)}")
    print("Merkle Tree module OK.")
