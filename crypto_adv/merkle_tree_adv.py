"""Merkle tree with inclusion proofs."""
from __future__ import annotations
import hashlib
from typing import List, Tuple


def _h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


class MerkleTree:
    def __init__(self, leaves: List[bytes]):
        self.leaves = [_h(x) for x in leaves]
        self.layers = [self.leaves[:]]
        layer = self.leaves[:]
        while len(layer) > 1:
            if len(layer) % 2:
                layer.append(layer[-1])
            next_layer = [_h(layer[i] + layer[i + 1]) for i in range(0, len(layer), 2)]
            self.layers.append(next_layer)
            layer = next_layer

    @property
    def root(self) -> bytes:
        return self.layers[-1][0] if self.layers else b""

    def proof(self, index: int) -> List[Tuple[bytes, str]]:
        proof = []
        for layer in self.layers[:-1]:
            sibling = index ^ 1
            if sibling < len(layer):
                side = "left" if sibling < index else "right"
                proof.append((layer[sibling], side))
            index //= 2
        return proof

    @staticmethod
    def verify(leaf: bytes, proof: List[Tuple[bytes, str]], root: bytes) -> bool:
        h = _h(leaf)
        for sibling, side in proof:
            h = _h(sibling + h) if side == "left" else _h(h + sibling)
        return h == root


if __name__ == "__main__":
    t = MerkleTree([b"a", b"b", b"c", b"d"])
    p = t.proof(0)
    assert MerkleTree.verify(b"a", p, t.root)
    print(f"merkle_tree_adv root={t.root[:4].hex()}")
    print("merkle_tree_adv self-tests passed")
