"""
Universe Simulator - Cartesian Tree
Original stack-based construction from sequence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CNode:
    value: int
    index: int
    left: Optional["CNode"] = None
    right: Optional["CNode"] = None


def build_cartesian(arr: List[int]) -> Optional[CNode]:
    if not arr:
        return None
    root = None
    stack: List[CNode] = []
    for i, v in enumerate(arr):
        last = None
        while stack and stack[-1].value > v:
            last = stack.pop()
        node = CNode(value=v, index=i)
        if stack:
            stack[-1].right = node
        else:
            root = node
        if last:
            node.left = last
        stack.append(node)
    return root


def inorder(node: Optional[CNode], out: List[int]) -> None:
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.value)
    inorder(node.right, out)


if __name__ == "__main__":
    arr = [9, 3, 7, 1, 8, 12, 10, 20, 15, 18, 5]
    root = build_cartesian(arr)
    assert root is not None and root.value == 1
    seq: List[int] = []
    inorder(root, seq)
    assert seq == sorted(arr)
    print("cartesian_tree self-test passed", root.value)
